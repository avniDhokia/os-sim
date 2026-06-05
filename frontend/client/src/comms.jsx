
export function sendNewProcess(name){
  fetch("http://127.0.0.1:5000/addProcess", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: name })
  })
  .catch(console.error);
}

export async function sendKillProcess(id){
  const res = await fetch("http://127.0.0.1:5000/killProcess", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: id })
  })
  .catch(console.error);

  if (res.ok){
    return {ok: true, message:"Process Killed"}
  }

  let data = await res.json();
  return {ok:false, message: data.message}
}


export function sendChangeScheduler(scheduler){
  fetch("http://127.0.0.1:5000/changeScheduler", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scheduler: scheduler })
  })
  .catch(console.error);
}