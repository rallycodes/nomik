#!/usr/bin/env node

/**
 * Nomik CLI
 * Author: Raul Aliyev (@rallycodes)
 * Zero-dependency CLI runner and agent skill installer.
 */

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const ROOT_DIR = path.resolve(__dirname, '..');
const SCRIPTS_DIR = path.join(ROOT_DIR, 'scripts');

function printBanner() {
  console.log(`
\x1b[35m _   _  ____  __  __ ___ _  __\x1b[0m
\x1b[35m| \\ | |/ __ \\|  \\/  |_ _| |/ /\x1b[0m
\x1b[35m|  \\| | |  | | |\\/| || || ' / \x1b[0m
\x1b[35m| |\\  | |__| | |  | || || . \\ \x1b[0m
\x1b[35m|_| \\_|\\____/|_|  |_|___|_|\\_\\\x1b[0m
\x1b[1m\x1b[36mNomik: The Billion-Dollar Brand Naming & Domain Engine\x1b[0m
\x1b[90mCreated by Raul Aliyev (@rallycodes) | Open Source MIT\x1b[0m
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

function installSkill(isGlobal = true) {
  printBanner();
  console.log('\x1b[32mInstalling Nomik Skill for AI Agents...\x1b[0m\n');

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
      const scripts = fs.readdirSync(SCRIPTS_DIR);
      for (const s of scripts) {
        if (!s.endsWith('.pyc') && !s.startsWith('__pycache__')) {
          fs.copyFileSync(path.join(SCRIPTS_DIR, s), path.join(target, 'scripts', s));
        }
      }

      // Copy references
      const refDir = path.join(ROOT_DIR, 'references');
      if (fs.existsSync(refDir)) {
        for (const r of fs.readdirSync(refDir)) {
          fs.copyFileSync(path.join(refDir, r), path.join(target, 'references', r));
        }
      }

      console.log(`\x1b[32m✓ Installed at:\x1b[0m ${target}`);
    } catch (err) {
      console.warn(`\x1b[33m! Warning installing to ${target}:\x1b[0m ${err.message}`);
    }
  }

  console.log(`
\x1b[1m\x1b[32m[SUCCESS] Nomik is now active in your AI agent environment!\x1b[0m
Type \x1b[1m\x1b[36m/nomik\x1b[0m in Claude Code, Antigravity, or Cursor to launch the agency.
`);
}

function printHelp() {
  printBanner();
  console.log(`\x1b[1mUSAGE:\x1b[0m
  \x1b[36mnpx nomik <brand>\x1b[0m              Run full audit (Domains + Handles + Phonetics)
  \x1b[36mnpx nomik install\x1b[0m              Install /nomik skill into AI agents globally
  \x1b[36mnpx nomik domain <brand>\x1b[0m       Check exact domains & pricing across TLDs
  \x1b[36mnpx nomik handles <brand>\x1b[0m      Check GitHub, npm, PyPI, and Crates.io handles
  \x1b[36mnpx nomik tm <brand>\x1b[0m           Run trademark knockout clearance check
  \x1b[36mnpx nomik phonetics <brand>\x1b[0m    Score phonosemantics, cadence & Radio Test

\x1b[1mEXAMPLES:\x1b[0m
  npx nomik kyntic
  npx nomik stripe.com
  npx nomik install
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
    installSkill();
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
