import FloorPlan from "./FloorPlan";

function RouteView({ result }) {
  const { route, unplaced, not_found } = result;
  return (
    <div>
      {route.length > 0 && <FloorPlan route={route} />}
      <ol className="route">
        {route.map((stop) => (
          <li key={stop.label}>
            <span className="aisle">{stop.label}</span>
            <span>{stop.items.map((i) => i.name).join(", ")}</span>
          </li>
        ))}
      </ol>
      {unplaced.length > 0 && (
        <p className="note">No aisle info (ask in store): {unplaced.join(", ")}</p>
      )}
      {not_found.length > 0 && (
        <p className="note warn">Not found: {not_found.join(", ")}</p>
      )}
    </div>
  );
}

export default RouteView;
