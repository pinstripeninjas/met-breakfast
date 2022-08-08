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
		container.innerHTML = `Server was busy, couldn't pull data :(`;
	}
};

loadImg("skewT");
loadImg("four_panel");

// load current date
const currentDate = new Date();
document.getElementById("current-date").textContent = new Intl.DateTimeFormat("en-US", {
	dateStyle: "full",
}).format(currentDate);
