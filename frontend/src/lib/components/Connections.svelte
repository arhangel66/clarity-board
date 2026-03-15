<script lang="ts">
    import { derived } from "svelte/store";
    import { cardsById, connections } from "../stores/cards";
    import type { Connection } from "../types";

    let containerWidth = $state(0);
    let containerHeight = $state(0);

    // Computed connections with coordinates
    const visibleConnections = derived(
        [connections, cardsById],
        ([$connections, $cardsById]) => {
            return $connections
                .map((conn) => {
                    const fromCard = $cardsById.get(conn.from_id);
                    const toCard = $cardsById.get(conn.to_id);

                    if (!fromCard || !toCard) return null;

                    return {
                        ...conn,
                        fromX: fromCard.x,
                        fromY: fromCard.y,
                        toX: toCard.x,
                        toY: toCard.y,
                    };
                })
                .filter(
                    (
                        c,
                    ): c is Connection & {
                        fromX: number;
                        fromY: number;
                        toX: number;
                        toY: number;
                    } => c !== null,
                );
        },
    );

    function getPath(conn: {
        fromX: number;
        fromY: number;
        toX: number;
        toY: number;
        type: string;
    }) {
        if (containerWidth === 0 || containerHeight === 0) return "";

        // Convert % to pixels
        const x1 = (conn.fromX / 100) * containerWidth;
        const y1 = (conn.fromY / 100) * containerHeight;
        const x2 = (conn.toX / 100) * containerWidth;
        const y2 = (conn.toY / 100) * containerHeight;

        // Bezier curve: quadratic Bezier with control point offset from midpoint
        const midX = (x1 + x2) / 2;
        const midY = (y1 + y2) / 2;

        // Offset control point slightly to create a curve
        const dx = x2 - x1;
        const dy = y2 - y1;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const offset = Math.min(dist * 0.2, 50); // limit curve depth

        // Normal vector for offset
        const nx = -dy / dist;
        const ny = dx / dist;

        const cpX = midX + nx * offset;
        const cpY = midY + ny * offset;

        return `M ${x1} ${y1} Q ${cpX} ${cpY} ${x2} ${y2}`;
    }

    // Connection Styles
    // causes: solid arrow
    // relates: dashed
    // contradicts: red with X (maybe just red line)
    // blocks: thick line

    function getStrokeDashArray(type: string): string {
        if (type === "relates") return "5, 5";
        return "";
    }

    function getStrokeColor(type: string): string {
        if (type === "contradicts") return "var(--danger)";
        if (type === "blocks") return "var(--text-medium)";
        if (type === "causes") return "var(--text-light)";
        return "var(--text-subtle)";
    }

    function getStrokeWidth(type: string, strength: number = 0.5): number {
        const base = type === "blocks" ? 4 : 2;
        return base + strength * 2;
    }
</script>

<div
    class="connections-container"
    bind:clientWidth={containerWidth}
    bind:clientHeight={containerHeight}
>
    <svg>
        <defs>
            <marker
                id="arrowhead"
                markerWidth="10"
                markerHeight="7"
                refX="28"
                refY="3.5"
                orient="auto"
                markerUnits="userSpaceOnUse"
            >
                <polygon points="0 0, 10 3.5, 0 7" fill="var(--text-light)" />
            </marker>
            <marker
                id="arrowhead-red"
                markerWidth="10"
                markerHeight="7"
                refX="28"
                refY="3.5"
                orient="auto"
                markerUnits="userSpaceOnUse"
            >
                <polygon points="0 0, 10 3.5, 0 7" fill="var(--danger)" />
            </marker>
        </defs>

        {#each $visibleConnections as conn (conn.id)}
            <path
                d={getPath(conn)}
                stroke={getStrokeColor(conn.type)}
                stroke-width={getStrokeWidth(conn.type, conn.strength)}
                stroke-dasharray={getStrokeDashArray(conn.type)}
                fill="none"
                marker-end={conn.type === "causes"
                    ? "url(#arrowhead)"
                    : conn.type === "contradicts"
                      ? "url(#arrowhead-red)"
                      : ""}
                class="connection-line"
            />

            <!-- Label -->
            {#if conn.label}
                <!-- Position text at midpoint -->
                <text
                    x={((conn.fromX + conn.toX) / 2 / 100) * containerWidth}
                    y={((conn.fromY + conn.toY) / 2 / 100) * containerHeight -
                        5}
                    text-anchor="middle"
                    class="connection-label"
                >
                    {conn.label}
                </text>
            {/if}
        {/each}
    </svg>
</div>

<style>
    .connections-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none; /* Let clicks pass through to background/cards */
        z-index: 5; /* Below cards (10), above background */
    }

    svg {
        width: 100%;
        height: 100%;
        overflow: visible;
    }

    .connection-line {
        transition: d 0.1s linear; /* Smooth updates when dragging */
        opacity: 0.6;
    }

    .connection-label {
        font-size: 11px;
        fill: var(--text-light);
        font-family: "Inter", sans-serif;
        text-shadow:
            0 1px 2px var(--bg-page),
            0 -1px 2px var(--bg-page),
            1px 0 2px var(--bg-page),
            -1px 0 2px var(--bg-page);
    }
</style>
