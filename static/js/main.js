url ="http://localhost:5000/";

labelsX = ["a", "b", "c", "d", "e", "f", "g", "h"];
labelsY = ["1", "2", "3", "4", "5", "6", "7", "8"];

pieceCodes = ["r", "n", "b", "q", "k", "p", "R", "N", "B", "Q", "K", "P"];

player = "white";

highlight = [];

movesInPos = [];

selected = "";

function move(move) {
	fetch(url + move);
	if(player == "white") {
		player == "black";
	} else {
		player == "white";
	}
}

function drawBoard(imgs, fen) {

	squaresToHighlight = [];
	if(highlight.length > 0) {
		for(i = 0; i < highlight.length; i++) {
			squaresToHighlight.push(highlight[i].slice(2, 4));
		}
		
	}

	clear();
	ranks = fen.split(" ")[0].split("/")

	count = 0;
	for(y = 0; y < 8; y++) {
		for(x = 0; x < 8; x++) {
			if(count % 2 == 0) {
				fill(255);
			} else {
				fill(0);
			}
			currentSquare = labelsX[x] + labelsY[7-y];
			if(squaresToHighlight.includes(currentSquare)) {
				fill(255, 0, 0);
			}
			rect(x * width/8, y * height/8, width/8, height/8);
			count ++;
		}
		count++;
	}

	out = ["", "", "", "", "", "", "", ""];

	for(i = 0; i < 8; i++) {
		rank = ranks[i];

		f = 0;
		while(f < 8) {
			item = rank[f];
			if(pieceCodes.includes(item)) {
				out[i] += item;
			} else {
				for(j = 0; j < parseInt(item); j++) {
					out[i] += " ";
				}
			}
			f++;
		}
	}
	for(i = 0; i < 8; i++) {
		for(j = 0; j < 8; j++) {
			if(out[i][j] != " ") {
				image(imgs[out[i][j]], width/8 * j, height/8 * i, width/8, height/8);
			}
		}
	}
}

imgs = {};
function setup() {
  createCanvas(800, 800);

	for(i = 0; i < pieceCodes.length; i++) {
		if(checkCase(pieceCodes[i]) == 0) {
			imgs[pieceCodes[i]] = loadImage("/static/assets/b" + pieceCodes[i] + ".png");
		} else {
			imgs[pieceCodes[i]] = loadImage("/static/assets/w" + pieceCodes[i].toLowerCase() + ".png");
		}
	}
  
}

function mouseClicked() {
	currentSquare = labelsX[Math.floor(mouseX/100)] + labelsY[7-Math.floor(mouseY/100)];	


	if(highlight.length > 0) {

		if(selected == currentSquare) {
			hightlight = [];
			selected = "";
			return 0;
		}

		movesForSquare = [];
		for(i = 0; i < movesInPos.length; i++) {
			startSquare = movesInPos[i].substring(0, 2);
			if(startSquare == selected) {
				movesForSquare.push(movesInPos[i]);
			}
		}

		moveToMake = [];
		for(i = 0; i < movesForSquare.length; i++) {
			if(movesForSquare[i].indexOf(currentSquare) > -1) {
				moveToMake.push(movesForSquare[i]);
			}
		}

		if(moveToMake.length == 0) {
			selected = [];
			hightlight= "";
		}

		if(moveToMake.length = 1) {
			fetch(url + "move/" + moveToMake[0]);
			highlight = [];
			selected = "";
		}

	} else {
		selected = currentSquare;

		movesForSquare = [];
		for(i = 0; i < movesInPos.length; i++) {
			startSquare = movesInPos[i].substring(0, 2);
			if(startSquare == currentSquare) {
				movesForSquare.push(movesInPos[i]);
			}
		}
		console.log(movesForSquare);
		highlight = movesForSquare;
		drawBoard(imgs, FEN);
		return false;
	}
}

function checkCase(c){
    var u = c.toUpperCase();
    return (c.toLowerCase() === u ? -1 : (c === u ? 1 : 0));
};

FEN = "";
function startup() {
	
	var eventSource = new EventSource("/stream")
	eventSource.onmessage = function(e) {
		FEN = e.data;

		fetch(url + 'legalMoves')
			.then(response => response.json())
			.then(data => {
				movesInPos = data;
		});

		drawBoard(imgs, e.data);
	};


	// setInterval(function() {
	// 	fetch('http://localhost:5000/legalMoves')
	// 		.then(response => response.json())
	// 		.then(data => {
	// 			move = data[Math.floor(Math.random() * data.length)];
	// 			console.log(move);
	// 			fetch("http://localhost:5000/move/" + move);
		
	// 		});
	// }, 10000);
}
