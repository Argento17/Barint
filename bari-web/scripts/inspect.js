const fs = require("fs");
const lines = fs.readFileSync("scripts/mk-expand.js", "utf8").split("\n");
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes("`")) console.log(i+1, lines[i].slice(0,100));
}
