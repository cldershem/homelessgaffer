var boardSize = 10;
var tileSize = 50/2;   //divided for more simple testing
var tileMargin = 5;
var tileLineWidth = 0;
var boardCoords = {};
var shipMargin = 25;
var boardMargin = (tileMargin * 10) + (tileSize * 10) + shipMargin;
var isSetUp = false;

var boardStage = new Kinetic.Stage({
    container: 'boardContainer',
    width: (tileMargin * 12) + (tileSize * 12) + (shipMargin * 2),
    height: (tileMargin * 11) + (tileSize * 10)
});

var gridLayer = new Kinetic.Layer();
var statusLayer = new Kinetic.Layer();
var shipLayer = new Kinetic.Layer();

var createBoardCoords = function() {
    var tileX = tileStartX = tileMargin; // horizontal
    var tileY = tileStartY = tileMargin; // vertical
        
    for (var row=0; row<boardSize; row++) {
        for (var col=0; col<boardSize; col++) {
            var coordName = row + "x" + col;
            boardCoords[coordName] = {
                coordX: row,
                coordY: col,
                startX: tileX,
                startY: tileY,
                endX: tileX + tileSize + (tileLineWidth * 2),
                endY: tileY + tileSize + (tileLineWidth * 2),
                status: ""
            };
            tileX += tileMargin + tileSize;
        };
        tileX = tileStartX;
        tileY += tileMargin + tileSize;
    };
};

var getGridCoords = function() {
    mousePos = boardStage.getMousePosition();
    mousePosX = mousePos.x;
    mousePosY = mousePos.y;
    gridCoord = "None";
    for (coord in boardCoords) {
        if (mousePosX >= boardCoords[coord].startX && mousePosX <= boardCoords[coord].endX) {
            if (mousePosY >= boardCoords[coord].startY && mousePosY <= boardCoords[coord].endY) {
                gridCoord = [boardCoords[coord].coordX + "x" + boardCoords[coord].coordY];
                break;
            };
        };
    };
};

var drawBoard = function(boardCoords) { 
    for (boardCoord in boardCoords) {   
        var rect = new Kinetic.Rect({
            x: boardCoords[boardCoord].startX,
            y: boardCoords[boardCoord].startY,
            width: tileSize,
            height: tileSize,
            stroke: 'black'
        });
        rect.on('mouseover', function() {
            this.setFill('blue');
            gridLayer.draw();
        });
        rect.on('mouseout', function() {
            this.setFill('clear');
            gridLayer.draw();
        });
        rect.on('mousedown', function() {
            this.setFill('red');
            gridLayer.draw();
            getGridCoords();
            setUpOrGame(gridCoord);
        });
        gridLayer.add(rect);
    };
    boardStage.add(gridLayer);
};

var setUpOrGame = function(gridCoord) {
    //~ if (isSetUp === true) {
        checkGuess(gridCoord);
    //~ } else {
        //~ setUpGame();
        //~ isSetUp = true;
    //~ };
};

var checkGuess = function(guessCoord) {
    if (boardCoords[guessCoord].status === "" || boardCoords[guessCoord].status === "miss") {
        boardCoords[guessCoord].status = "guessed";
        isMiss(guessCoord);
    } else if (boardCoords[guessCoord].status === "guessed" || boardCoords[guessCoord].status === "hit") {
        alert("guessed");
    } else if (boardCoords[guessCoord].status === "ship") {
        boardCoords[guessCoord].status = "hit";
        isHit(guessCoord);
    };
};

var isMiss = function(gridCoord) {
    var startX = boardCoords[gridCoord].startX;
    var startY = boardCoords[gridCoord].startY;
    var endX = boardCoords[gridCoord].endX;
    var endY = boardCoords[gridCoord].endY;
    
    var missX = new Kinetic.Line({
        points: [startX, startY, endX, endY],
        stroke: 'red'
    });
    
    var missY = new Kinetic.Line({
        points: [startX, endY, endX, startY],
        stroke: 'red'
    });
    
    statusLayer.add(missX);
    statusLayer.add(missY);
    statusLayer.draw();
    boardStage.add(statusLayer);
    writeMessage("You missed");
};

var isHit = function(gridCoord) {
    var startX = boardCoords[gridCoord].startX + (tileSize/2);
    var startY = boardCoords[gridCoord].startY + (tileSize/2);

    var drawHit = new Kinetic.Circle({
        x: startX,
        y: startY,
        radius: (tileSize/2),
        fill: 'blue',
        stroke: 'red',
    });
    
    statusLayer.add(drawHit);
    boardStage.add(statusLayer);
    writeMessage("You hit a ship");
};

var setUpGame = function() {
    createBoardCoords();
    drawBoard(boardCoords);
    boardCoords["0x0"].status = "ship";
    boardCoords["0x1"].status = "ship";
    boardCoords["4x4"].status = "ship";
    boardCoords["5x4"].status = "ship";
    boardCoords["6x4"].status = "ship";
    boardCoords["7x4"].status = "ship";
    writeMessage("Board has been setup.");
};

var writeMessage = function(message) {
    $message = message;
    $(document).ready(function(message) {
        $('#messages ul').append('<li>' + $message + '</li>');
    });
    $("#messages").scrollTop($("#messages")[0].scrollHeight);
};

var shipFleet = {
    patrolBoat: {
        "name": "Patrol Boat",
        "size": 2,
        "numOfShips": 1,
        "harborX": boardMargin,
        "harborY": tileMargin
    },
    patrolBoat2: {
        "name": "Patrol Boat",
        "size": 2,
        "numOfShips": 1,
        "harborX": boardMargin,
        "harborY": (tileMargin * 2 + shipMargin) + (tileSize * 2)
    },
    submarine: {
        "name": "Submarine",
        "size": 3,
        "numOfShips": 1,
        "harborX": boardMargin + shipMargin + (tileSize),
        "harborY": tileMargin
    },
    battleship: {
        "name": "Battleship",
        "size": 4,
        "numOfShips": 1,
        "harborX": boardMargin,
        "harborY": (tileMargin * 3) + (shipMargin * 2) + (tileSize * 4)
    },
    aircraftCarrier: {
        "name": "Aircraft Carrier",
        "size": 5,
        "numOfShips": 1,
        "harborX": boardMargin + shipMargin + (tileSize),
        "harborY": (tileMargin * 3) + shipMargin + (tileSize * 3)
    }
};

var drawShipFleet = function() {

    for (ship in shipFleet) {
        tileX = shipFleet[ship].harborX;
        tileY = shipFleet[ship].harborY;
        groupName = new Kinetic.Group({
            draggable: true,
            id: ship,
            //offset: [tileX, tileY]
        });
        for (i=0; i<shipFleet[ship].size; i++) {
            var rect = new Kinetic.Rect({
            x: tileX,
            y: tileY,
            width: tileSize,
            height: tileSize,
            stroke: 'black',
            fill: 'green',
            });
            groupName.add(rect);
            tileY += tileSize + tileMargin;
        };
        var indrag = false;  //separates click from drag
        groupName.on('dragstart', function() {
            indrag = true;
        });        
        groupName.on('dragend', function() {
            var shipName = this.getId();
            var groupX = this.getPosition().x + shipFleet[shipName].harborX;
            var groupY = this.getPosition().y + shipFleet[shipName].harborY;
            // snap to grid
            writeMessage(groupX + "," + groupY + " " + shipName + ".");
            indrag = false;
        });
        groupName.on('click', function(evt) {
            var ship = this.getId();
            if (indrag) { // separtes click from drag
                return;
            } else {
                //rotate ship
                oldX = this.getPosition().x + shipFleet[ship].harborX;
                oldY = this.getPosition().y + shipFleet[ship].harborY;
                //writeMessage(this.getOffset().x + " , " + this.getOffset.Y + "offset old ");
                this.setOffset([oldX, oldY]);                
                //writeMessage(this.getOffset().x + " , " + this.getOffset.Y + "offset new ");
                
                writeMessage(oldX + " , " + oldY + "-------oldXandY");
                writeMessage(this.getPosition().x);
                var angleToAdd = this.getRotationDeg() + 90;
                this.setRotationDeg(angleToAdd);
                //this.setOffset([0,0]);
                this.setPosition([100, 100]);
                writeMessage(this.getPosition().x + " , " + this.getPosition().y);
            };
        });
        shipLayer.add(groupName);
    };
    boardStage.add(shipLayer);
};

setUpGame();
drawShipFleet();
