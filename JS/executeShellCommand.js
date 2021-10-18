// executes shell command from Node
const execSync = require('child_process').execSync;
commandStr = 'ls'
const output = execSync(commandStr, { encoding: 'utf-8' });