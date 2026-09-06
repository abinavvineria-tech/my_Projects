// LilyNova App — Modulaire, intégrée avec Hermes Agent
const app = {
  currentPage: 'overview',
  theme: 'dark',
  projects: [],
  
  init() {
    this.loadTheme();
    this.setupKeyboard();
    this.renderOverview();
    this.updateStats();
    this.startClock();
    this.setupCommandPalette();
    this.notify('LilyNova active. Welcome, abinav!', 'success');
  },
  navigate(page) {
    this.currentPage = page;
    document.querySelectorAll('.sidebar-item').forEach(b => b.classList.remove('active'));
    document.querySelector(`[data-page="${page}"]`)?.classList.add('active');
    document.getElementById('status-location').textContent = page.charAt(0).toUpperCase() + page.slice(1);
    
    const content = document.getElementById('content');
    content.innerHTML = '';
    
    switch(page) {
      case 'overview': this.renderOverview(); break;
      case 'studio': this.renderStudio(); break;
      case 'timebreaker': this.renderTimebreaker(); break;
      case 'purelily': this.renderPureLily(); break;
      case 'cookierun': this.renderCookieRun(); break;
      case 'hermes': this.renderHermes(); break;
      case 'projects': this.renderProjects(); break;
      case 'terminal': this.renderTerminal(); break;
      case 'settings': this.renderSettings(); break;
    }
  },
  renderOverview() {
    document.getElementById('content').innerHTML = `
      <div class="grid grid-cols-3 gap-4 mb-6">
        ${this.card('Status', 'Active', 'All systems operational', 'fa-check-circle').outerHTML}
        ${this.card('Tasks', '3 Running', 'Studio, Timebreaker, Docs', 'fa-tasks').outerHTML}
        ${this.card('Agent', 'Online', 'Hermes Agent integrated', 'fa-robot').outerHTML}
      </div>
      <h2 class="text-xl font-bold mb-4">Recent Activity</h2>
      <div class="grid grid-cols-2 gap-4">
        <div class="card rounded-xl p-4">
          <h3 class="font-semibold mb-2">Project Scaffolding</h3>
          <p class="text-sm text-lily-lavender/80">LilyNova ecosystem initialized at <code>/Projects/lilynova</code>. Modular architecture ready.</p>
          <div class="flex gap-2 mt-3">
            <button onclick="app.navigate('projects')" class="btn-primary px-3 py-1 rounded-md text-xs">Open Projects</button>
            <button onclick="app.notify('Creating project...','info')" class="px-3 py-1 rounded-md text-xs bg-lily-mid">New Project</button>
          </div>
        </div>
        <div class="card rounded-xl p-4">
          <h3 class="font-semibold mb-2">Hermes Integration</h3>
          <p class="text-sm text-lily-lavender/80">Skill <code>lilynova</code> created. Safety rules configured (confirm destructive ops).</p>
          <button onclick="app.notify('Skill verified','success')" class="btn-primary px-3 py-1 rounded-md text-xs mt-3">Verify Skill</button>
        </div>
      </div>
    `;
  },
  card(title, stat, desc, icon) {
    const div = document.createElement('div');
    div.className = 'card rounded-xl p-4';
    div.innerHTML = `<h3 class="text-sm text-lily-lavender">${title}</h3><div class="text-2xl font-bold my-1">${stat}</div><div class="text-xs text-lily-lavender/60">${desc}</div>`;
    return div;
  },
  renderStudio() {
    document.getElementById('content').innerHTML = `<h2 class="text-xl font-bold mb-4">LilyNova Studio</h2>
    <div class="grid grid-cols-3 gap-4">
      ${this.card('New Project', 'Create', 'Scaffold with TypeScript + React + Tailwind', 'fa-plus').outerHTML}
      ${this.card('File Explorer', 'Browse', 'Navigate workspace files', 'fa-folder').outerHTML}
      ${this.card('Editor', 'Edit', 'Integrated code editor', 'fa-code').outerHTML}
      ${this.card('Terminal', 'CLI', 'Termux/Linux friendly sessions', 'fa-terminal').outerHTML}
      ${this.card('Preview', 'Render', 'Live preview panel', 'fa-eye').outerHTML}
      ${this.card('Templates', 'Select', 'Project templates', 'fa-layer-group').outerHTML}
    </div>`;
  },
  renderTimebreaker() {
    document.getElementById('content').innerHTML = `<h2 class="text-xl font-bold mb-4">Timebreaker Workspace</h2>
    <p class="text-sm text-lily-lavender/70 mb-4">Language workspace, compiler, LSP-oriented architecture.</p>
    <div class="card rounded-xl p-4"><h3 class="font-semibold">Compiler</h3><button onclick="app.notify('Timebreaker compiler ready','success')" class="btn-primary px-3 py-1 rounded-md text-xs mt-2">Run Compiler</button></div>`;
  },
  renderPureLily() {
    document.getElementById('content').innerHTML = `<h2 class="text-xl font-bold mb-4">PureLily</h2>
    <div class="grid grid-cols-3 gap-4">
      <div class="card rounded-xl p-4"><h3 class="font-semibold">Creative Workspace</h3><p class="text-xs mt-2">Purple, pink, gold aesthetic.</p></div>
      <div class="card rounded-xl p-4"><h3 class="font-semibold">Tools & Utilities</h3></div>
      <div class="card rounded-xl p-4"><h3 class="font-semibold">Theme Engine</h3><p class="text-xs mt-2">Glassmorphism + dark/light.</p></div>
    </div>`;
  },
  renderCookieRun() {
    document.getElementById('content').innerHTML = `<h2 class="text-xl font-bold mb-4">Cookie Run Workspace</h2>
    <div class="grid grid-cols-2 gap-4">
      <div class="card rounded-xl p-4"><h3 class="font-semibold">CRK Projects</h3><p class="text-xs">Fan/development focused.</p></div>
      <div class="card rounded-xl p-4"><h3 class="font-semibold">Cookie Run Crumble</h3><p class="text-xs">Creative projects.</p></div>
      <div class="card rounded-xl p-4"><h3 class="font-semibold">Typing Game Projects</h3></div>
      <div class="card rounded-xl p-4"><h3 class="font-semibold">Creative Tools</h3></div>
    </div>`;
  },
  renderHermes() {
    document.getElementById('content').innerHTML = `<h2 class="text-xl font-bold mb-4">Hermes Agent</h2>
    <div class="card rounded-xl p-4 mb-4"><h3 class="font-semibold">Status</h3><div class="flex gap-4 mt-2"><span class="text-green-400">● Online</span><span>Model: openrouter</span><span>Profile: everlily</span></div></div>
    <div class="grid grid-cols-3 gap-4">
      <div class="card rounded-xl p-4"><h3 class="font-semibold">Skills</h3><p>lilynova (new)</p><p>cookie-run-kingdom-cookie-checker</p><p>hermes-agent</p></div>
      <div class="card rounded-xl p-4"><h3 class="font-semibold">Tasks</h3><p>3 active</p><p>Dashboard, Skill, Project</p></div>
      <div class="card rounded-xl p-4"><h3 class="font-semibold">Configuration</h3><p>Preserves existing dashboard</p></div>
    </div>`;
  },
  renderProjects() { 
    document.getElementById('content').innerHTML = `<h2 class="text-xl font-bold mb-4">Projects</h2><div class="grid grid-cols-2 gap-4"><div class="card rounded-xl p-4"><h3>lilynova</h3><p class="text-xs">Next-gen ecosystem</p><button onclick="app.notify('Project open: lilynova','success')" class="btn-primary px-3 py-1 rounded-md text-xs mt-2">Open</button></div></div>`; 
  },
  renderTerminal() { 
    document.getElementById('content').innerHTML = `<h2 class="text-xl font-bold mb-4">Terminal</h2><div class="terminal-bg rounded-xl p-4 font-mono text-sm h-64 overflow-auto">$ ls Projects/<br>lilynova  hermes-workspace  hermes-webui<br>$ echo "LilyNova ready"</div>`; 
  },
  renderSettings() { 
    document.getElementById('content').innerHTML = `<h2 class="text-xl font-bold mb-4">Settings</h2>
    <div class="card rounded-xl p-4 mb-4"><h3 class="font-semibold">Theme</h3><div class="flex gap-2 mt-2"><button onclick="app.toggleTheme();app.notify('Theme switched','info')" class="btn-primary px-3 py-1 rounded-md">Toggle</button></div></div>`; 
  },
  
  // Command Palette
  setupCommandPalette() {
    const input = document.getElementById('command-input');
    input.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase();
      const cmds = [
        {name:'Go to Overview', cmd:'nav:overview'},
        {name:'Go to Studio', cmd:'nav:studio'},
        {name:'Go to Timebreaker', cmd:'nav:timebreaker'},
        {name:'New Project', cmd:'action:new'},
        {name:'Open Terminal', cmd:'nav:terminal'},
        {name:'Toggle Theme', cmd:'action:theme'},
        {name:'Notify Test', cmd:'action:notify'},
      ].filter(c => c.name.toLowerCase().includes(q));
      document.getElementById('command-results').innerHTML = cmds.map(c => `<button onclick="app.execCommand('${c.cmd}')" class="command-item w-full text-left p-3 flex items-center gap-3 border-b border-lily-lavender/10 text-sm"><i class="fas fa-arrow-right text-lily-pink"></i><span>${c.name}</span></button>`).join('');
    });
    input.addEventListener('keydown', e => { if(e.key==='Enter') { const first = document.querySelector('.command-item'); if(first) first.click(); } if(e.key==='Escape') this.closeCommandPalette(); });
  },
  execCommand(cmd) {
    if(cmd.startsWith('nav:')) this.navigate(cmd.split(':')[1]);
    else if(cmd==='action:new') this.notify('New project dialog (simulated)','info');
    else if(cmd==='action:theme') this.toggleTheme();
    else if(cmd==='action:notify') this.notify('Test notification','success');
    this.closeCommandPalette();
  },
  toggleCommandPalette() { document.getElementById('command-palette').classList.toggle('hidden'); if(!document.getElementById('command-palette').classList.contains('hidden')) { setTimeout(() => document.getElementById('command-input').focus(), 100); } },
  closeCommandPalette() { document.getElementById('command-palette').classList.add('hidden'); },
  
  // Theme / Keyboard / Clock
  toggleTheme() { document.body.classList.toggle('light'); document.body.classList.toggle('dark'); this.theme = this.theme==='dark'?'light':'dark'; document.getElementById('theme-icon').className = this.theme==='dark'?'fas fa-moon':'fas fa-sun'; },
  loadTheme() { this.theme='dark'; document.getElementById('theme-icon').className='fas fa-moon'; },
  setupKeyboard() { document.addEventListener('keydown', e => { if(e.ctrlKey && e.key==='k') { e.preventDefault(); this.toggleCommandPalette(); } if(e.key==='Escape') this.closeCommandPalette(); }); },
  startClock() { setInterval(() => document.getElementById('status-time').textContent = new Date().toLocaleTimeString(), 1000); },
  
  updateStats() { document.getElementById('stat-projects').textContent = 1; document.getElementById('stat-tasks').textContent = 3; document.getElementById('stat-skills').textContent = 3 + 1; },
  notify(msg, type='info') { 
    const n = document.createElement('div'); 
    n.className = 'notification glass rounded-lg p-3 shadow-xl text-sm max-w-xs'; 
    const color = type==='success'?'text-green-400':type==='error'?'text-red-400':'text-lily-pink'; 
    n.innerHTML = `<div class="flex items-center gap-2 ${color}"><i class="fas fa-bell"></i><span>${msg}</span></div>`; 
    document.getElementById('notifications').appendChild(n); 
    setTimeout(() => n.remove(), 4000); 
  },
};
document.addEventListener('DOMContentLoaded', () => app.init());
