#!/usr/bin/env node

/**
 * Nomik CLI
 * Author: Raul Aliyev (@rallycodes)
 * Zero-dependency CLI runner, brand auditor, and agent skill updater.
 */

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const https = require('https');

const ROOT_DIR = path.resolve(__dirname, '..');
const SCRIPTS_DIR = path.join(ROOT_DIR, 'scripts');

function printBanner() {
  console.log(`
\x1b[38;2;168;85;247m  █▄ █ █▀█ █▀▄▀█ █ █▄▀\x1b[0m
\x1b[38;2;99;102;241m  █ ▀█ █▄█ █ ▀ █ █ █ █\x1b[0m
\x1b[1m\x1b[37m  N O M I K\x1b[0m \x1b[90m— Billion-Dollar Brand Naming & Domain Engine\x1b[0m
\x1b[38;2;16;185;129m  ● The AI skill that named itself\x1b[0m \x1b[90m• by Raul Aliyev (@rallycodes)\x1b[0m
`);
}

function runPython(scriptName, args = []) {
  const scriptPath = path.join(SCRIPTS_DIR, scriptName);
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
  const result = spawnSync(pythonCmd, [scriptPath, ...args], {
    stdio: 'inherit',
    shell: true
  });
  return result.status;
}

function copyRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  const stats = fs.statSync(src);
  if (stats.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const child of fs.readdirSync(src)) {
      if (child !== '__pycache__' && !child.endsWith('.pyc')) {
        copyRecursive(path.join(src, child), path.join(dest, child));
      }
    }
  } else {
    fs.copyFileSync(src, dest);
  }
}

function installSkill(isUpdate = false) {
  printBanner();
  const actionWord = isUpdate ? 'Updating' : 'Installing';
  console.log(`\x1b[32m${actionWord} Nomik Skill for AI Agents...\x1b[0m\n`);

  const targets = [];
  
  // Workspace target
  const workspaceTarget = path.join(process.cwd(), '.agents', 'skills', 'nomik');
  targets.push(workspaceTarget);

  // Global target
  const homeDir = os.homedir();
  const globalTarget = path.join(homeDir, '.agents', 'skills', 'nomik');
  targets.push(globalTarget);

  for (const target of targets) {
    try {
      fs.mkdirSync(target, { recursive: true });
      fs.mkdirSync(path.join(target, 'scripts'), { recursive: true });
      fs.mkdirSync(path.join(target, 'references'), { recursive: true });
      fs.mkdirSync(path.join(target, 'evals'), { recursive: true });

      // Copy SKILL.md
      fs.copyFileSync(path.join(ROOT_DIR, 'SKILL.md'), path.join(target, 'SKILL.md'));

      // Copy scripts
      copyRecursive(SCRIPTS_DIR, path.join(target, 'scripts'));

      // Copy references
      const refDir = path.join(ROOT_DIR, 'references');
      if (fs.existsSync(refDir)) {
        copyRecursive(refDir, path.join(target, 'references'));
      }

      // Copy evals
      const evalDir = path.join(ROOT_DIR, 'evals');
      if (fs.existsSync(evalDir)) {
        copyRecursive(evalDir, path.join(target, 'evals'));
      }

      console.log(`\x1b[32m✓ Synchronized at:\x1b[0m ${target}`);
    } catch (err) {
      console.warn(`\x1b[33m! Warning updating ${target}:\x1b[0m ${err.message}`);
    }
  }

  const successMessage = isUpdate
    ? `\x1b[1m\x1b[32m[SUCCESS] Nomik skill updated to the latest version!\x1b[0m`
    : `\x1b[1m\x1b[32m[SUCCESS] Nomik is now active in your AI agent environment!\x1b[0m`;

  console.log(`
${successMessage}
Type \x1b[1m\x1b[36m/nomik\x1b[0m in Claude Code, Antigravity, or Cursor to launch the agency.
`);
}

function updateSkill() {
  // If running inside a git repo of nomik, pull latest first
  if (fs.existsSync(path.join(ROOT_DIR, '.git'))) {
    console.log('\x1b[90mChecking for git updates from origin...\x1b[0m');
    spawnSync('git', ['pull', 'origin', 'main'], { cwd: ROOT_DIR, stdio: 'inherit' });
  }
  installSkill(true);
}

function printHelp() {
  printBanner();
  console.log(`\x1b[1mCOMMANDS:\x1b[0m
  \x1b[36mnpx nomik <brand>\x1b[0m              Run full audit (Domains + Handles + Phonetics + Trademarks)
  \x1b[36mnpx nomik install\x1b[0m              Install /nomik skill into AI agents globally
  \x1b[36mnpx nomik update\x1b[0m               Update Nomik skill to the latest version
  \x1b[36mnpx nomik domain <brand>\x1b[0m       Check exact domains & pricing across TLDs
  \x1b[36mnpx nomik handles <brand>\x1b[0m      Check GitHub, npm, PyPI, and Crates.io handles
  \x1b[36mnpx nomik tm <brand>\x1b[0m           Run trademark knockout clearance check
  \x1b[36mnpx nomik phonetics <brand>\x1b[0m    Score phonosemantics, cadence & visual rhythm

\x1b[1mEXAMPLES:\x1b[0m
  npx nomik kyntic
  npx nomik stripe.com
  npx nomik install
  npx nomik update
`);
}

function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === 'help' || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  if (command === 'install') {
    installSkill(false);
    return;
  }

  if (command === 'update' || command === 'upgrade') {
    updateSkill();
    return;
  }

  if (command === 'domain' || command === 'domains') {
    const brand = args[1];
    if (!brand) {
      console.error('Error: specify a brand or domain name (e.g. npx nomik domain kyntic)');
      process.exit(1);
    }
    if (brand.includes('.')) {
      runPython('check_domain.py', [brand]);
    } else {
      runPython('check_domain.py', ['--brand', brand]);
    }
    return;
  }

  if (command === 'handles' || command === 'handle') {
    const handle = args[1];
    if (!handle) {
      console.error('Error: specify a handle (e.g. npx nomik handles kyntic)');
      process.exit(1);
    }
    runPython('check_handles.py', [handle]);
    return;
  }

  if (command === 'tm' || command === 'trademark') {
    const brand = args[1];
    if (!brand) {
      console.error('Error: specify a brand name (e.g. npx nomik tm kyntic)');
      process.exit(1);
    }
    runPython('check_trademark.py', [brand]);
    return;
  }

  if (command === 'phonetics' || command === 'phonetic') {
    const brand = args[1];
    if (!brand) {
      console.error('Error: specify a brand name (e.g. npx nomik phonetics kyntic)');
      process.exit(1);
    }
    runPython('phonetics.py', [brand]);
    return;
  }

  // Default: audit brand completely
  const brand = command;
  printBanner();
  console.log(`\x1b[1mRunning Comprehensive Brand Audit for:\x1b[0m \x1b[36m${brand.toUpperCase()}\x1b[0m\n`);
  
  if (brand.includes('.')) {
    runPython('check_domain.py', [brand]);
  } else {
    runPython('check_domain.py', ['--brand', brand]);
    runPython('check_handles.py', [brand]);
    runPython('phonetics.py', [brand]);
    runPython('check_trademark.py', [brand]);
  }
}

main();
