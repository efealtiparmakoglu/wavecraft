import test from 'node:test';
import assert from 'node:assert/strict';
import { createFrameClock } from '../timing.mjs';

test('ship movement integrates the same time at 60 Hz and 144 Hz', () => {
  const distances = [60, 144].map(rate => {
    const clock = createFrameClock(0);
    let distance = 0;
    for (let frame = 1; frame <= rate * 2; frame++) {
      distance += 2 * clock.tick(frame * 1000 / rate).delta;
    }
    return distance;
  });
  for (const distance of distances) assert.ok(Math.abs(distance - 4) < 1e-10);
  assert.ok(Math.abs(distances[0] - distances[1]) < 1e-10);
});

test('FPS reports the actual number of frames over the measurement interval', () => {
  for (const rate of [30, 60, 144]) {
    const clock = createFrameClock(0);
    const samples = [];
    for (let frame = 1; frame <= rate * 2; frame++) {
      const { fps } = clock.tick(frame * 1000 / rate);
      if (fps !== null) samples.push(fps);
    }
    assert.ok(samples.length >= 4);
    for (const fps of samples) assert.ok(Math.abs(fps - rate) < 1e-9);
  }
});

test('returning from a paused tab caps movement without losing elapsed time', () => {
  const clock = createFrameClock(1000);
  const next = clock.tick(6000);
  assert.equal(next.delta, 0.05);
  assert.equal(next.elapsed, 5);
  assert.equal(clock.tick(6016).delta, 0.016);
});
