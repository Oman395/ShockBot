import Avrgirl from "avrgirl-arduino";

const boardName = process.argv[2];

function flashBoard(boardType) {
  return new Promise((resolve, reject) => {
    let avrgirl = new Avrgirl({
      board: boardType,
      debug: true
    });
    avrgirl.flash(`./compiled/${boardType}.hex`, (error) => {
      if (error) return reject(error);
      resolve();
    });
  });
}

console.log(`Flashing to ${boardName}...`);
flashBoard(boardName);
