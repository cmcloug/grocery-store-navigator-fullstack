async function request(url, options) {
  let res;
  try {
    res = await fetch(url, options);
  } catch {
    throw new Error("Can't reach the server. Is the backend running?");
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
  return data;
}

export const fetchStores = (zip) =>
  request(`/api/stores?zip=${encodeURIComponent(zip)}`).then((d) => d.stores);

export const fetchRoute = (storeId, items) =>
  request("/api/route", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ store_id: storeId, items }),
  });
