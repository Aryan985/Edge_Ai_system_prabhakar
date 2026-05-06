setInterval(() => {
    fetch('/status')
    .then(res => res.json())
    .then(data => {

        const status = document.getElementById("status");

        document.getElementById("distance").innerText = data.distance;

        if(data.danger){
            status.innerText = "DANGER ⚠️";
            status.style.color = "red";
        } else {
            status.innerText = "SAFE ✅";
            status.style.color = "green";
        }
    });

}, 500);