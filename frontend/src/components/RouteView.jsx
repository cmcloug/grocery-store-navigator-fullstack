function RouteView({ result }) {
  const { route, unplaced, not_found } = result;
  return (
    <div>
      <ol className="route">
        {route.map((stop) => (
          <li key={stop.aisle}>
            <span className="aisle">Aisle {stop.aisle}</span>
            <span>{stop.items.join(", ")}</span>
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
