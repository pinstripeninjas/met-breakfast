// const skewT = document.createElement("img");
// skewT.src = "https://picsum.photos/200/301";

// document.querySelector(".empty-box").innerHTML = "";
// document.querySelector(".empty-box").append(skewT);
// document.body.append(skewT);

// function to receive img blob from API and display image
const loadImg = async (containerId) => {
	const url = `${window.location.origin}/img/${containerId}`;
	const container = document.getElementById(containerId);
	let response = await fetch(url);
	if (response.status === 200) {
		const imgText = await response.text();
		container.innerHTML = imgText;
	} else {
		console.log(`HTTP-Error: ${response.status}`);
		container.innerHTML = `It didn't work :(`;
	}
};

loadImg("skewT");
