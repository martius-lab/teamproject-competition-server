import { readFileSync } from 'fs';
import { parse } from 'toml';

export function parseArgs() {
    const args = {};;
    process.argv
        .slice(2, process.argv.length)
        .forEach(arg => {
            const longArg = arg.split('=');
            args[longArg[0]] = longArg[1];
        });
    return args;
}

export function parseConfig() {
    const args = parseArgs();
    console.log(args);
    const configFilePath = args['config'] || 'config.toml';
    try {
        console.log('Reading configuration file:', configFilePath);
        const tomlData = readFileSync(configFilePath, 'utf8');
        const parsedData = parse(tomlData);
        const str = JSON.stringify(parsedData)
        return JSON.parse(str);
    } catch (error) {
        console.error('Error reading the configuration file:', error);
        return null;
    }
}

export const config = parseConfig();