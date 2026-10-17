import { useState } from "react";
import StoreCard from "../components/StoreCard";
import GroceryList from "../components/GroceryList";
import RouteView from "../components/RouteView";
import { fetchStores, fetchRoute } from "../api";

function Home() {
  const [zip, setZip] = useState("");
  const [stores, setStores] = useState([]);
  const [store, setStore] = useState(null);
  const [items, setItems] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function run(task) {
    setLoading(true);
    setError("");
    try {
      await task();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  const searchStores = (e) => {
    e.preventDefault();
    run(async () => {
      const found = await fetchStores(zip.trim());
      setStores(found);
      setStore(null);
      setResult(null);
      if (!found.length) throw new Error("No stores found for that ZIP code.");
    });
  };

  const planRoute = () =>
    run(async () => setResult(await fetchRoute(store.id, items)));

  return (
    <div className="home">
      <header>
        <h1>🛒 Grocery Store Navigator</h1>
        <p>Find your store, add your list, and walk the aisles in order.</p>
      </header>

      {error && <p className="error" role="alert">{error}</p>}

      <section>
        <h2>1. Find a store</h2>
        <form className="row" onSubmit={searchStores}>
          <input
            value={zip}
            onChange={(e) => setZip(e.target.value)}
            placeholder="ZIP code"
            inputMode="numeric"
            maxLength={5}
            aria-label="ZIP code"
          />
          <button type="submit" disabled={loading || zip.trim().length !== 5}>
            Search
          </button>
        </form>
        <div className="stores-grid">
          {stores.map((s) => (
            <StoreCard
              store={s}
              key={s.id}
              selected={store?.id === s.id}
              onSelect={(picked) => {
                setStore(picked);
                setResult(null);
              }}
            />
          ))}
        </div>
      </section>

      {store && (
        <section>
          <h2>2. Your grocery list</h2>
          <GroceryList items={items} onChange={setItems} />
          <button
            className="primary"
            onClick={planRoute}
            disabled={loading || !items.length}
          >
            {loading ? "Working…" : "Plan my route"}
          </button>
        </section>
      )}

      {result && (
        <section>
          <h2>3. Your route</h2>
          <RouteView result={result} />
        </section>
      )}
    </div>
  );
}

export default Home;
