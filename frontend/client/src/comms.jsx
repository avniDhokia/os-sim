
export function sendNewProcess(name){
  fetch("http://127.0.0.1:5000/addProcess", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: name })
  })
  .catch(console.error);
}

export function sendKillProcess(id){
  fetch("http://127.0.0.1:5000/killProcess", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: id })
  })
  .catch(console.error);
}


export function sendChangeScheduler(scheduler){
  fetch("http://127.0.0.1:5000/changeScheduler", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scheduler: scheduler })
  })
  .catch(console.error);
}