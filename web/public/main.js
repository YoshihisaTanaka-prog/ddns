$("#restart").on("click", ()=>{
  fetch("/stop", {
    method: 'POST',
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({test: "test"})
  }).then((response) => response.json()).then((data) =>{
    console.log(data)
  })
});