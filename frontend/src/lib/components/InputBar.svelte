<script lang="ts">
  import { onMount } from "svelte";
  import { websocket } from "../stores/websocket";
  import { session } from "../stores/session";
  import { strings } from "../stores/i18n";
  import { auth } from "../stores/auth";
  import { API_BASE } from "../config";

  let inputText = $state("");
  let isRecording = $state(false);
  let isTranscribing = $state(false);
  let micError = $state<string | null>(null);
  let isVoiceMode = $state(true);
  let pendingSpecialQuestion = $state<{
    id: string;
    question: string;
    hint: string;
  } | null>(null);
  let mediaRecorder: MediaRecorder | null = null;
  let mediaStream: MediaStream | null = null;
  let chunks: BlobPart[] = [];
  let mimeType = "";
  let inputEl: HTMLInputElement | null = null;

  let authToken = $state<string | null>(null);

  $effect(() => {
    const unsubscribe = session.subscribe((state) => {
      pendingSpecialQuestion = state.pendingSpecialQuestion;
    });
    return unsubscribe;
  });

  $effect(() => {
    const unsubscribe = auth.subscribe((state) => {
      authToken = state.token;
    });
    return unsubscribe;
  });

  onMount(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (!isVoiceMode || isRecording || isTranscribing) return;
      if (event.code !== "Space" || event.repeat) return;
      const target = event.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === "INPUT" ||
          target.tagName === "TEXTAREA" ||
          target.isContentEditable)
      ) {
        return;
      }
      event.preventDefault();
      startRecording(event);
    }

    function handleKeyUp(event: KeyboardEvent) {
      if (!isVoiceMode) return;
      if (event.code !== "Space") return;
      const target = event.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === "INPUT" ||
          target.tagName === "TEXTAREA" ||
          target.isContentEditable)
      ) {
        return;
      }
      event.preventDefault();
      stopRecording(event);
    }

    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  });

  function handleSend() {
    const text = inputText.trim();
    if (!text) return;

    if (pendingSpecialQuestion) {
      websocket.sendTextWithSpecialQuestion(text, pendingSpecialQuestion.id);
      session.clearPendingSpecialQuestion();
    } else {
      websocket.sendText(text);
    }
    inputText = "";
  }

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  function getSupportedMimeType(): string {
    const types = [
      "audio/webm;codecs=opus",
      "audio/webm",
      "audio/ogg;codecs=opus",
      "audio/ogg",
    ];
    for (const type of types) {
      if (MediaRecorder.isTypeSupported(type)) {
        return type;
      }
    }
    return "";
  }

  async function startRecording(event?: Event) {
    event?.preventDefault();
    if (isRecording || isTranscribing) return;

    micError = null;

    if (!navigator.mediaDevices?.getUserMedia) {
      micError = $strings.input.voiceErrorUnavailable;
      return;
    }
    if (typeof MediaRecorder === "undefined") {
      micError = $strings.input.voiceErrorUnavailable;
      return;
    }

    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mimeType = getSupportedMimeType();
      mediaRecorder = new MediaRecorder(
        mediaStream,
        mimeType ? { mimeType } : undefined,
      );
      chunks = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          chunks.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: mimeType || "audio/webm" });
        chunks = [];
        await transcribeAudio(blob);
      };

      mediaRecorder.start();
      isRecording = true;
    } catch (error) {
      console.error("Microphone access failed", error);
      micError = $strings.input.voiceErrorPermission;
      cleanupRecording();
    }
  }

  async function stopRecording(event?: Event) {
    event?.preventDefault();
    if (!isRecording) return;
    isRecording = false;
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
    } else {
      cleanupRecording();
    }
  }

  function cleanupRecording() {
    if (mediaRecorder) {
      mediaRecorder.ondataavailable = null;
      mediaRecorder.onstop = null;
      mediaRecorder = null;
    }
    if (mediaStream) {
      for (const track of mediaStream.getTracks()) {
        track.stop();
      }
      mediaStream = null;
    }
  }

  async function transcribeAudio(blob: Blob) {
    if (!blob.size) {
      cleanupRecording();
      return;
    }

    isTranscribing = true;

    const extension = blob.type.includes("ogg") ? "ogg" : "webm";
    const formData = new FormData();
    formData.append("file", blob, `ptt.${extension}`);

    try {
      const response = await fetch(`${API_BASE}/api/transcribe`, {
        method: "POST",
        headers: authToken
          ? { Authorization: `Bearer ${authToken}` }
          : undefined,
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Transcription failed: ${response.status}`);
      }

      const data = await response.json();
      const text = typeof data?.text === "string" ? data.text.trim() : "";

      if (text) {
        if (pendingSpecialQuestion) {
          websocket.sendTextWithSpecialQuestion(
            text,
            pendingSpecialQuestion.id,
          );
          session.clearPendingSpecialQuestion();
        } else {
          websocket.sendText(text);
        }
      }
    } catch (error) {
      console.error("Transcription failed", error);
      micError = $strings.input.voiceErrorTranscription;
    } finally {
      isTranscribing = false;
      cleanupRecording();
    }
  }

  function getVoiceTitle(): string {
    if (micError) return micError;
    if (isTranscribing) return $strings.input.voiceTitleTranscribing;
    if (isRecording) return $strings.input.voiceTitleRecording;
    return $strings.input.voiceTitleIdle;
  }

  function toggleInputMode() {
    isVoiceMode = !isVoiceMode;
    if (!isVoiceMode) {
      setTimeout(() => inputEl?.focus(), 0);
    }
  }

  function getToggleTitle(): string {
    return isVoiceMode
      ? $strings.input.toggleToText
      : $strings.input.toggleToVoice;
  }
</script>

<div class="input-dock">
  <!-- Voice Capsule -->
  <div class="capsule" class:expanded={!isVoiceMode}>
    <!-- Text Input Area (Hidden by default) -->
    {#if !isVoiceMode}
      <div class="text-input-group">
        <button
          class="utility-btn"
          onclick={toggleInputMode}
          title={$strings.input.toggleToVoice}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>
        <input
          type="text"
          class="text-input"
          placeholder={$strings.input.placeholderDefault}
          bind:value={inputText}
          bind:this={inputEl}
          onkeydown={handleKeyDown}
          disabled={isRecording || isTranscribing}
        />
        <button
          class="send-btn"
          onclick={handleSend}
          disabled={!inputText.trim()}
        >
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    {/if}

    <!-- Voice Mode / Mic Button (Always Visible or Toggled) -->
    {#if isVoiceMode}
      <div class="mic-container">
        <button
          class="mic-btn"
          class:recording={isRecording}
          class:transcribing={isTranscribing}
          onpointerdown={startRecording}
          onpointerup={stopRecording}
          onpointerleave={stopRecording}
          onpointercancel={stopRecording}
          title={getVoiceTitle()}
        >
          {#if isTranscribing}
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M5 12h14"></path>
              <path d="M12 5v14"></path>
            </svg>
          {:else if isRecording}
            <div
              style="width: 20px; height: 20px; background: white; border-radius: 4px;"
            ></div>
          {:else}
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"
              ></path>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
              <line x1="12" y1="19" x2="12" y2="23"></line>
              <line x1="8" y1="23" x2="16" y2="23"></line>
            </svg>
          {/if}
          <span class="mic-tooltip">
            {isRecording
              ? $strings.input.voiceStatusListening
              : $strings.input.voiceHint}
          </span>
        </button>
      </div>

      <button
        class="utility-btn"
        onclick={toggleInputMode}
        title={getToggleTitle()}
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path d="M4 7V4h16v3"></path>
          <path d="M9 20h6"></path>
          <path d="M12 4v16"></path>
        </svg>
      </button>
    {/if}
  </div>
</div>

<style>
  /* Voice First Capsule Design */
  .input-dock {
    position: fixed;
    bottom: 32px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
    width: auto;
    max-width: 90vw;
  }

  .capsule {
    position: relative;
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 999px;
    padding: 6px;
    box-shadow:
      0 10px 40px -10px rgba(0, 0, 0, 0.15),
      0 0 0 1px rgba(0, 0, 0, 0.05);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .capsule.expanded {
    padding: 6px 6px 6px 16px;
    background: white;
    box-shadow:
      0 20px 40px -10px rgba(0, 0, 0, 0.2),
      0 0 0 1px rgba(0, 0, 0, 0.08);
  }

  /* --- Main Mic Button --- */
  .mic-container {
    position: relative;
    z-index: 2;
  }

  .mic-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    border: none;
    border-radius: 50%;
    background: var(--question-purple);
    color: white;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .mic-btn:hover {
    transform: scale(1.05);
    background: #7e57c2;
  }

  .mic-btn:active {
    transform: scale(0.95);
  }

  .mic-btn.recording {
    background: #ef4444;
    box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4);
    transform: scale(1.1);
  }

  .mic-btn.transcribing {
    background: #f59e0b;
    animation: spin-pulse 2s infinite;
  }

  /* --- Text Input Section --- */
  .text-input-group {
    display: flex;
    align-items: center;
    gap: 8px;
    width: 0;
    opacity: 0;
    overflow: hidden;
    transition: all 0.3s ease;
  }

  .capsule.expanded .text-input-group {
    width: 320px;
    opacity: 1;
    margin-right: 8px;
  }

  .text-input {
    flex: 1;
    border: none;
    background: transparent;
    font-size: 16px;
    color: var(--text-dark);
    min-width: 0;
    padding: 8px 0;
    outline: none;
  }

  .send-btn {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: rgba(0, 0, 0, 0.05);
    border-radius: 50%;
    color: var(--text-dark);
    cursor: pointer;
    transition: all 0.2s;
  }

  .send-btn:hover:not(:disabled) {
    background: #dcfce7;
    color: #166534;
  }

  .send-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  /* --- Toggle / Utility Buttons --- */
  .utility-btn {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: transparent;
    border-radius: 50%;
    color: var(--text-medium);
    cursor: pointer;
    transition: all 0.2s;
  }

  .utility-btn:hover {
    background: rgba(0, 0, 0, 0.05);
    color: var(--text-dark);
  }

  /* --- Tooltips --- */
  .mic-tooltip {
    position: absolute;
    top: -40px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.2s;
    white-space: nowrap;
  }

  .mic-btn:hover .mic-tooltip,
  .mic-btn.recording .mic-tooltip {
    opacity: 1;
  }

  @keyframes spin-pulse {
    0% {
      box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4);
    }
    70% {
      box-shadow: 0 0 0 10px rgba(245, 158, 11, 0);
    }
    100% {
      box-shadow: 0 0 0 0 rgba(245, 158, 11, 0);
    }
  }

  @media (max-width: 600px) {
    .capsule.expanded .text-input-group {
      width: 200px;
    }
  }
</style>
