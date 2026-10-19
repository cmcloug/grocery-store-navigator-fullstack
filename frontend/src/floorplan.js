// Builds a schematic store layout and walking path from the route.
// Kroger gives only aisle/bay/side per product, not a real floor plan, so this
// is an approximation: numbered aisles run front-to-back, produce (aisle 0)
// sits on the left wall, and other departments line the back wall.

export const AISLE_W = 34;
export const TOP = 56; // back-wall walking lane
export const HEIGHT = 380;
export const BOTTOM = HEIGHT - 56; // front walking lane (entrance/checkout)
export const SIDE = 70; // width of the left/right lanes
const MAX_BAY = 50;

const SHELF_TOP = TOP + 28;
const SHELF_BOTTOM = BOTTOM - 16;

export function buildFloorPlan(route) {
  const aisleStops = route.filter((s) => !s.department);
  const maxAisle = Math.max(8, ...aisleStops.map((s) => s.number));
  const width = SIDE * 2 + maxAisle * AISLE_W;
  const leftX = SIDE / 2;
  const rightX = width - SIDE / 2;
  const aisleX = (n) => SIDE + (n - 0.5) * AISLE_W;

  const wallDepts = route.filter((s) => s.department && s.number < 100);
  const backDepts = route.filter((s) => s.department && s.number >= 100);

  const placed = route.map((stop) => {
    if (!stop.department) {
      return {
        stop,
        points: stop.items.map((item) => {
          const frac = item.bay == null ? 0.5 : Math.min(item.bay, MAX_BAY) / MAX_BAY;
          const y = SHELF_BOTTOM - frac * (SHELF_BOTTOM - SHELF_TOP);
          const offset = item.side === "L" ? -6 : item.side === "R" ? 6 : 0;
          return { x: aisleX(stop.number), dotX: aisleX(stop.number) + offset, y, dotY: y };
        }),
      };
    }
    const wall = stop.number < 100;
    const list = wall ? wallDepts : backDepts;
    const i = list.indexOf(stop);
    const t = (i + 1) / (list.length + 1);
    const p = wall
      ? { x: leftX, y: TOP + t * (BOTTOM - TOP) }
      : { x: SIDE + t * (width - 2 * SIDE), y: TOP };
    return { stop, points: [{ ...p, dotX: p.x, dotY: p.y }] };
  });

  const entrance = { x: leftX, y: BOTTOM };
  const checkout = { x: rightX, y: BOTTOM };
  const path = [entrance];
  let at = entrance;
  const visit = (target) => {
    for (const p of connect(at, target)) push(path, p);
    at = target;
  };
  for (const { points } of placed) for (const p of points) visit(p);
  visit(checkout);

  return { width, leftX, rightX, maxAisle, aisleX, placed, path, entrance, checkout };
}

// Walk orthogonally: straight when sharing a lane, otherwise out to the
// nearer of the front/back cross lanes, across, then in.
function connect(a, b) {
  if (a.x === b.x || (a.y === b.y && (a.y === TOP || a.y === BOTTOM))) return [b];
  const lane =
    Math.abs(a.y - TOP) + Math.abs(b.y - TOP) <=
    Math.abs(a.y - BOTTOM) + Math.abs(b.y - BOTTOM)
      ? TOP
      : BOTTOM;
  return [{ x: a.x, y: lane }, { x: b.x, y: lane }, b];
}

function push(path, p) {
  const last = path[path.length - 1];
  if (last.x !== p.x || last.y !== p.y) path.push({ x: p.x, y: p.y });
}
