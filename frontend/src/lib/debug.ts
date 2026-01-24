/// <reference types="vite/client" />
/**
 * Debug utilities for development.
 * Send logs to debug server for inspection.
 */

const DEBUG_SERVER = 'http://127.0.0.1:5656';
const DEBUG_ENABLED = import.meta.env.DEV;

interface DebugPayload {
  msg: string;
  data?: unknown;
  source?: string;
  timestamp?: string;
}

/**
 * Send debug log to debug server.
 * Only works in development mode.
 */
export function debugLog(msg: string, data?: unknown): void {
  if (!DEBUG_ENABLED) return;

  const payload: DebugPayload = {
    msg,
    data,
    source: 'frontend',
    timestamp: new Date().toISOString(),
  };

  // Also log to console
  console.log(`[DEBUG] ${msg}`, data);

  // Send to debug server (fire and forget)
  fetch(`${DEBUG_SERVER}/log`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  }).catch(() => {
    // Debug server might not be running, ignore
  });
}

/**
 * Create a debug logger with a prefix.
 */
export function createDebugLogger(prefix: string) {
  return (msg: string, data?: unknown) => debugLog(`[${prefix}] ${msg}`, data);
}
