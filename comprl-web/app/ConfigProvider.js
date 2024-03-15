import { readFileSync } from 'fs';
import { parse } from 'toml';
const configFilePath = 'config.toml';
let configData;
try {
    const tomlData = readFileSync(configFilePath, 'utf8');
    const parsedData = parse(tomlData);
    configData = JSON.stringify(parsedData);
    configData = JSON.parse(configData);
} catch (error) {
    console.error('Error reading the configuration file:', error);
    process.exit(1);
}


export const config = configData;