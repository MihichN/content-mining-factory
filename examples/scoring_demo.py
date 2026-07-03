#!/usr/bin/env python3
"""Illustrative highlight scoring demo (standalone, no dependencies).

This is a simplified excerpt of the scoring concept used in the private
Content Mining Factory pipeline. It shows how multi-signal weights produce
a viral score and how nearby peaks are clustered into clip candidates.

Run: python examples/scoring_demo.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SignalScores:
    audio_spike: float = 0.0
    laughter: float = 0.0
    motion: float = 0.0
    keyword_hit: float = 0.0
    scene_change: float = 0.0


@dataclass
class ScoringWeights:
    audio_spike: float
    laughter: float
    motion: float
    keyword_hit: float
    scene_change: float


STREAMER_CLIP = ScoringWeights(
    audio_spike=25,
    laughter=25,
    motion=15,
    keyword_hit=20,
    scene_change=10,
)


def compute_viral_score(signals: SignalScores, weights: ScoringWeights) -> float:
    total = (
        signals.audio_spike * weights.audio_spike
        + signals.laughter * weights.laughter
        + signals.motion * weights.motion
        + signals.keyword_hit * weights.keyword_hit
        + signals.scene_change * weights.scene_change
    )
    return round(total, 2)


def cluster_peaks(
    timeline: dict[float, SignalScores],
    merge_window_sec: float = 8.0,
    min_score: float = 40.0,
) -> list[tuple[float, float, float]]:
    """Merge nearby signal peaks → (start, end, score)."""
    if not timeline:
        return []

    times = sorted(timeline.keys())
    clusters: list[list[float]] = [[times[0]]]
    for t in times[1:]:
        if t - clusters[-1][-1] <= merge_window_sec:
            clusters[-1].append(t)
        else:
            clusters.append([t])

    results: list[tuple[float, float, float]] = []
    for cluster in clusters:
        merged = SignalScores()
        for t in cluster:
            s = timeline[t]
            merged.audio_spike = max(merged.audio_spike, s.audio_spike)
            merged.laughter = max(merged.laughter, s.laughter)
            merged.motion = max(merged.motion, s.motion)
            merged.keyword_hit = max(merged.keyword_hit, s.keyword_hit)
            merged.scene_change = max(merged.scene_change, s.scene_change)

        score = compute_viral_score(merged, STREAMER_CLIP)
        if score >= min_score:
            start = max(0.0, min(cluster) - 2.0)
            end = max(cluster) + 5.0
            results.append((start, end, score))

    return sorted(results, key=lambda x: x[2], reverse=True)


def main() -> None:
    # Mock timeline: seconds → normalized signal strengths (0..1)
    timeline = {
        12.0: SignalScores(audio_spike=0.9, laughter=0.7),
        14.0: SignalScores(audio_spike=0.8, laughter=0.85, keyword_hit=0.6),
        45.0: SignalScores(motion=0.5, scene_change=0.4),
        90.0: SignalScores(audio_spike=0.95, laughter=0.9, motion=0.6),
        92.0: SignalScores(keyword_hit=0.8, laughter=0.75),
        180.0: SignalScores(motion=0.3),
    }

    highlights = cluster_peaks(timeline, min_score=35.0)

    print("Content Mining Factory — scoring demo\n")
    print(f"Profile: streamer_clip  |  peaks: {len(timeline)}  |  highlights: {len(highlights)}\n")
    for i, (start, end, score) in enumerate(highlights, 1):
        print(f"  #{i}  {start:5.1f}s – {end:5.1f}s   score={score:6.1f}")


if __name__ == "__main__":
    main()
