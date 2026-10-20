// Keep animation delta separate from the HUD's FPS sampling interval.
export function createFrameClock(startMs) {
  let previousMs = startMs;
  let sampleStartMs = startMs;
  let frames = 0;

  return {
    tick(nowMs) {
      const delta = Math.min(0.05, Math.max(0, (nowMs - previousMs) / 1000));
      previousMs = nowMs;
      frames += 1;
      let fps = null;
      const sampleDuration = nowMs - sampleStartMs;
      if (sampleDuration >= 400) {
        fps = frames * 1000 / sampleDuration;
        sampleStartMs = nowMs;
        frames = 0;
      }
      return { elapsed: (nowMs - startMs) / 1000, delta, fps };
    },
  };
}
