import { useMemo } from "react";
import { buildFloorPlan, AISLE_W, TOP, BOTTOM, HEIGHT } from "../floorplan";

function FloorPlan({ route }) {
  const plan = useMemo(() => buildFloorPlan(route), [route]);
  const { width, leftX, aisleX, maxAisle, placed, path, entrance, checkout } = plan;
  const used = new Set(route.filter((s) => !s.department).map((s) => s.number));
  const d = path.map((p, i) => `${i ? "L" : "M"}${p.x} ${p.y}`).join(" ");

  return (
    <figure className="floorplan">
      <div className="floorplan-scroll">
        <svg
          viewBox={`0 0 ${width} ${HEIGHT}`}
          role="img"
          aria-label="Schematic store map with your walking route"
        >
          <rect className="fp-wall" x="2" y="2" width={width - 4} height={HEIGHT - 4} rx="10" />

          {Array.from({ length: maxAisle }, (_, i) => i + 1).map((n) => (
            <g key={n}>
              <rect
                className={`fp-shelf${used.has(n) ? " active" : ""}`}
                x={aisleX(n) - 9}
                y={TOP + 28}
                width="18"
                height={BOTTOM - TOP - 44}
                rx="3"
              />
              <text className="fp-aisle-label" x={aisleX(n)} y={TOP + 20} textAnchor="middle">
                {n}
              </text>
            </g>
          ))}

          <text className="fp-label" x={entrance.x} y={HEIGHT - 12} textAnchor="middle">
            Entrance
          </text>
          <text className="fp-label" x={checkout.x} y={HEIGHT - 12} textAnchor="middle">
            Checkout
          </text>

          <path className="fp-route" d={d} pathLength="1" />

          {placed.map(({ stop, points }, i) => (
            <g key={stop.label}>
              {points.map((p, j) => (
                <circle key={j} className="fp-dot" cx={p.dotX} cy={p.dotY} r="4" />
              ))}
              <g transform={`translate(${points[0].dotX} ${points[0].dotY})`}>
                <circle className="fp-badge" r="10" cy="-14" />
                <text className="fp-badge-text" y="-10" textAnchor="middle">
                  {i + 1}
                </text>
              </g>
              {stop.department && (
                <text
                  className="fp-label"
                  x={points[0].dotX + (points[0].x === leftX ? 16 : 0)}
                  y={points[0].dotY + (points[0].x === leftX ? 4 : -30)}
                  textAnchor={points[0].x === leftX ? "start" : "middle"}
                >
                  {stop.label}
                </text>
              )}
            </g>
          ))}
        </svg>
      </div>
      <figcaption>
        Schematic layout, not to scale. Aisle positions come from Kroger's aisle and bay
        numbers; the real store may differ.
      </figcaption>
    </figure>
  );
}

export default FloorPlan;
