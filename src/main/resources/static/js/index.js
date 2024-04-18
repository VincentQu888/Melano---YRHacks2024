const left = document.getElementById("left");

const handleOnMove = e => {
    const p = e.clientX / window.innerWidth*100;

    left.style.width = `${p}%`;
}

document.onmousemove = e => handleOnMove(e);