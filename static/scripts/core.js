// Menu stuff

const menuButton = document.querySelector("header > img");
const menuBack = document.querySelector(".menu > div > .top > img");
const menu = document.querySelector(".menu");

menuButton.addEventListener("click", () => {
	menu.style.right = "0";
});
menuBack.addEventListener("click", () => {
	menu.style.right = "-100%";
});

// Matrix stuff

const matrix = {
	width: 8,
	height: 8,
};
const matrixDiv = document.querySelector(".matrix");
for (let i = 0; i < matrix.height; i++) {
	const matrixRowDiv = document.createElement("div");
	matrixRowDiv.className = "row";
	for (let k = 0; k < matrix.width; k++) {
		const pixel = document.createElement("div");
		pixel.className = "led";
		matrixRowDiv.appendChild(pixel);
	}

	matrixDiv.appendChild(matrixRowDiv);
}

const ledDivs = Array.from(document.querySelectorAll(".row .led"))
const fetchLeds = async () => {
	const response = await fetch("/api/leds");
	const data = await response.json()

	return [response, data]
}

const decimalToRgb = (decimal) => {
	return [
	  (decimal >> 16) & 0xff,
	  (decimal >> 8) & 0xff,
	  decimal & 0xff,
	];
}
const updateMatrix = async () => {
	const [response, data] = await fetchLeds();

	ledDivs.forEach((led => {
		led.style.backgroundColor = "#c8c8c8"
	}))
	data.pixels.forEach((pixel) => {
		rgb = decimalToRgb(pixel.color)

		if ((parseInt(pixel.index / data.height) + 1) % 2 == 0){
			ledDivs[(parseInt(pixel.index / data.height) * data.height + data.width - (pixel.index % 8)) - 1].style.backgroundColor = `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, 1)`;
			return
		}
		ledDivs[pixel.index].style.backgroundColor = `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, 1)`;
	})
}

updateMatrix()
setInterval(updateMatrix, 100)