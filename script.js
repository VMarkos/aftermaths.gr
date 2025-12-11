const launchDate = new Date("Jan 1, 2026 00:00:00").getTime();

const x = setInterval(function() {

    const now = new Date().getTime();

    const distance = launchDate - now;

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
    const formatTime = (time) => String(time).padStart(2, '0');

    document.getElementById("days").innerHTML = formatTime(days);
    document.getElementById("hours").innerHTML = formatTime(hours);
    document.getElementById("minutes").innerHTML = formatTime(minutes);
    document.getElementById("seconds").innerHTML = formatTime(seconds);

    if (distance < 0) {
        clearInterval(x);
        document.getElementById("countdown").innerHTML = "Φτάσαμε!";
        document.getElementById("countdown").style.fontSize = "1.8em";
        document.getElementById("countdown").style.backgroundColor = "transparent";
        document.getElementById("countdown").style.color = "#007bff";
    }
}, 1000);
