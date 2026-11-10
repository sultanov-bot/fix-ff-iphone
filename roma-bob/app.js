const STORAGE_KEY = 'roma_bob_settings_v1';

const defaultState = {
  assist: true,
  headshot: 50,
  size: 60,
  opacity: 85,
  crossSize: 60,
  crossOpacity: 100,
  color: '#00dfff',
  bubbleFrozen: false,
  generalSens: 55,
  redDot: 62,
  scope2x: 48,
  scope4x: 58,
  sniper: 52,
  freeLook: 66,
  activeProfile: 'headshot',
  floatingR: { x: 28, y: 180, size: 60, opacity: 85, visible: false, frozen: false }
};

const state = { ...defaultState };

const refs = {
  crosshairCanvas: document.getElementById('crosshairCanvas'),
  rPreviewCanvas: document.getElementById('rPreviewCanvas'),
  floatingR: document.getElementById('floatingR'),
  rPanel: document.getElementById('rPanel'),
  statusBar: document.getElementById('statusBar'),
  assistToggle: document.getElementById('assistToggle'),
  headshot: document.getElementById('headshot'),
  headshotValue: document.getElementById('headshotValue'),
  buttonSize: document.getElementById('buttonSize'),
  buttonSizeValue: document.getElementById('buttonSizeValue'),
  buttonOpacity: document.getElementById('buttonOpacity'),
  buttonOpacityValue: document.getElementById('buttonOpacityValue'),
  crossSize: document.getElementById('crossSize'),
  crossSizeValue: document.getElementById('crossSizeValue'),
  crossOpacity: document.getElementById('crossOpacity'),
  crossOpacityValue: document.getElementById('crossOpacityValue'),
  floatingSize: document.getElementById('floatingSize'),
  floatingSizeValue: document.getElementById('floatingSizeValue'),
  floatingOpacity: document.getElementById('floatingOpacity'),
  floatingOpacityValue: document.getElementById('floatingOpacityValue'),
  generalSens: document.getElementById('generalSens'),
  generalSensValue: document.getElementById('generalSensValue'),
  redDot: document.getElementById('redDot'),
  redDotValue: document.getElementById('redDotValue'),
  scope2x: document.getElementById('scope2x'),
  scope2xValue: document.getElementById('scope2xValue'),
  scope4x: document.getElementById('scope4x'),
  scope4xValue: document.getElementById('scope4xValue'),
  sniper: document.getElementById('sniper'),
  sniperValue: document.getElementById('sniperValue'),
  freeLook: document.getElementById('freeLook'),
  freeLookValue: document.getElementById('freeLookValue'),
  saveSettings: document.getElementById('saveSettings'),
  resetApp: document.getElementById('resetApp'),
  freezeAim: document.getElementById('freezeAim'),
  hideAim: document.getElementById('hideAim'),
  shrinkCrosshair: document.getElementById('shrinkCrosshair'),
  growCrosshair: document.getElementById('growCrosshair'),
  freezeRButton: document.getElementById('freezeRButton'),
  closeRPanel: document.getElementById('closeRPanel')
};

function setStatus(text) {
  refs.statusBar.textContent = text;
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const saved = JSON.parse(raw);
    Object.assign(state, defaultState, saved);
    if (saved.floatingR) {
      state.floatingR = { ...defaultState.floatingR, ...saved.floatingR };
    }
  } catch (err) {
    console.warn('Unable to read settings', err);
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function bindRange(id, key, displayEl, formatter = (v) => `${v}%`) {
  const input = document.getElementById(id);
  input.addEventListener('input', (event) => {
    state[key] = Number(event.target.value);
    displayEl.textContent = formatter(state[key]);
    render();
  });
}

function applyStateToInputs() {
  refs.assistToggle.checked = state.assist;
  refs.headshot.value = state.headshot;
  refs.headshotValue.textContent = `${state.headshot}%`;
  refs.buttonSize.value = state.size;
  refs.buttonSizeValue.textContent = `${state.size}%`;
  refs.buttonOpacity.value = state.opacity;
  refs.buttonOpacityValue.textContent = `${state.opacity}%`;
  refs.crossSize.value = state.crossSize;
  refs.crossSizeValue.textContent = `${state.crossSize}%`;
  refs.crossOpacity.value = state.crossOpacity;
  refs.crossOpacityValue.textContent = `${state.crossOpacity}%`;
  refs.generalSens.value = state.generalSens;
  refs.generalSensValue.textContent = `${state.generalSens}%`;
  refs.redDot.value = state.redDot;
  refs.redDotValue.textContent = `${state.redDot}%`;
  refs.scope2x.value = state.scope2x;
  refs.scope2xValue.textContent = `${state.scope2x}%`;
  refs.scope4x.value = state.scope4x;
  refs.scope4xValue.textContent = `${state.scope4x}%`;
  refs.sniper.value = state.sniper;
  refs.sniperValue.textContent = `${state.sniper}%`;
  refs.freeLook.value = state.freeLook;
  refs.freeLookValue.textContent = `${state.freeLook}%`;
  refs.floatingSize.value = state.floatingR.size;
  refs.floatingSizeValue.textContent = `${state.floatingR.size}%`;
  refs.floatingOpacity.value = state.floatingR.opacity;
  refs.floatingOpacityValue.textContent = `${state.floatingR.opacity}%`;

  refs.floatingR.style.width = `${state.floatingR.size * 0.9}px`;
  refs.floatingR.style.height = `${state.floatingR.size * 0.9}px`;
  refs.floatingR.style.left = `${state.floatingR.x}px`;
  refs.floatingR.style.top = `${state.floatingR.y}px`;
  refs.floatingR.style.opacity = (state.floatingR.opacity / 100).toFixed(2);
  refs.floatingR.classList.toggle('hidden', !state.floatingR.visible || state.assist);
  refs.rPanel.classList.toggle('hidden', !state.floatingR.visible || state.assist);
}

function drawCrosshairPreview() {
  const canvas = refs.crosshairCanvas;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;
  const cx = w / 2;
  const cy = h / 2;
  const radius = Math.max(12, (state.crossSize / 100) * 48);

  ctx.clearRect(0, 0, w, h);

  ctx.save();
  ctx.translate(cx, cy);
  ctx.strokeStyle = state.color;
  ctx.lineWidth = 3;
  ctx.globalAlpha = state.crossOpacity / 100;
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, Math.PI * 2);
  ctx.stroke();

  ctx.strokeStyle = '#ff2c66';
  ctx.beginPath();
  ctx.moveTo(0, -radius - 10);
  ctx.lineTo(0, -radius + 9);
  ctx.moveTo(0, radius - 8);
  ctx.lineTo(0, radius + 10);
  ctx.moveTo(-radius - 10, 0);
  ctx.lineTo(-radius + 9, 0);
  ctx.moveTo(radius - 9, 0);
  ctx.lineTo(radius + 10, 0);
  ctx.stroke();

  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.arc(0, 0, 4.5, 0, Math.PI * 2);
  ctx.fill();

  ctx.restore();
}

function drawFloatingRCanvas() {
  const canvas = refs.rPreviewCanvas;
  const ctx = canvas.getContext('2d');
  const size = Math.max(32, (state.floatingR.size / 100) * 150);
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const r = size * 0.38;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.save();
  ctx.translate(cx, cy);
  ctx.globalAlpha = state.floatingR.opacity / 100;

  ctx.beginPath();
  ctx.arc(0, 0, r, 0, Math.PI * 2);
  ctx.fillStyle = '#ff2b5d';
  ctx.fill();
  ctx.lineWidth = 2;
  ctx.strokeStyle = '#ffc4d2';
  ctx.stroke();

  ctx.fillStyle = '#ffffff';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.font = `700 ${Math.max(24, size * 0.28)}px Arial`;
  ctx.fillText('R', 0, 2);
  ctx.restore();
}

function render() {
  drawCrosshairPreview();
  drawFloatingRCanvas();
  applyStateToInputs();
  updateProfileButtons();
}

function updateProfileButtons() {
  document.querySelectorAll('.profile-button').forEach((button) => {
    const isActive = button.dataset.profile === state.activeProfile;
    button.classList.toggle('active', isActive);
  });
}

function updateProfile(name) {
  const profileMap = {
    headshot: { headshot: 100 },
    oneTap: { headshot: 100 },
    dragShot: { headshot: 100 },
    rush: { headshot: 100 },
    proPlayer: { headshot: 100 },
    maxDrag: { headshot: 100 }
  };

  const profile = profileMap[name] || { headshot: 100 };
  state.headshot = profile.headshot;
  state.activeProfile = name;
  refs.headshot.value = state.headshot;
  refs.headshotValue.textContent = `${state.headshot}%`;
  setStatus(`Профиль: ${name.toUpperCase()}`);
  saveState();
  render();
}

function syncAssistState() {
  state.assist = refs.assistToggle.checked;
  state.floatingR.visible = !state.assist;
  if (state.assist) {
    refs.rPanel.classList.add('hidden');
    refs.floatingR.classList.add('hidden');
  } else {
    refs.rPanel.classList.add('hidden');
    refs.floatingR.classList.remove('hidden');
  }
  saveState();
  render();
}

function openGame(type) {
  const protocol = type === 'max' ? 'ffmax://' : 'ff://';
  const warningText = 'Прямой запуск Free Fire на iPhone не поддерживается через Safari. Откройте приложение через официальный способ запуска или установите игру и запустите её вручную.';

  const launchFrame = document.createElement('iframe');
  launchFrame.style.display = 'none';
  launchFrame.src = protocol;
  document.body.appendChild(launchFrame);

  setTimeout(() => {
    document.body.removeChild(launchFrame);
    setStatus(warningText);
  }, 1200);
}

function setColor(color) {
  state.color = color;
  document.querySelectorAll('.color-swatch').forEach((swatch) => {
    swatch.classList.toggle('active', swatch.dataset.color === color);
  });
  render();
}

function resetState() {
  if (!confirm('Сбросить все настройки?')) return;
  Object.assign(state, defaultState);
  localStorage.removeItem(STORAGE_KEY);
  render();
  setStatus('Сброшено');
}

function setFloatingSizeFromInput() {
  state.floatingR.size = Number(refs.floatingSize.value);
  state.floatingR.opacity = Number(refs.floatingOpacity.value);
  refs.floatingSizeValue.textContent = `${state.floatingR.size}%`;
  refs.floatingOpacityValue.textContent = `${state.floatingR.opacity}%`;
  refs.floatingR.style.width = `${state.floatingR.size * 0.9}px`;
  refs.floatingR.style.height = `${state.floatingR.size * 0.9}px`;
  refs.floatingR.style.opacity = (state.floatingR.opacity / 100).toFixed(2);
  render();
}

function freezeRPanel() {
  state.floatingR.frozen = !state.floatingR.frozen;
  refs.freezeRButton.textContent = state.floatingR.frozen ? 'РАЗМОРОЗИТЬ ПОЗИЦИЮ' : 'ЗАМОРОЗИТЬ ПОЗИЦИЮ';
  setStatus(state.floatingR.frozen ? 'Положение кнопки зафиксировано' : 'Перемещение снова доступно');
  render();
}

function showRPanel() {
  if (state.assist) return;
  state.floatingR.visible = true;
  refs.rPanel.classList.remove('hidden');
  refs.floatingR.classList.remove('hidden');
  saveState();
  render();
}

function hideRPanel() {
  refs.rPanel.classList.add('hidden');
  if (!state.assist) {
    state.floatingR.visible = true;
    refs.floatingR.classList.remove('hidden');
  }
  saveState();
  render();
}

function setFloatingButtonPosition(x, y) {
  state.floatingR.x = Math.max(10, Math.min(window.innerWidth - 80, x));
  state.floatingR.y = Math.max(28, Math.min(window.innerHeight - 80, y));
  refs.floatingR.style.left = `${state.floatingR.x}px`;
  refs.floatingR.style.top = `${state.floatingR.y}px`;
  saveState();
}

function attachFloatingRInteractions() {
  let dragging = false;
  let startX = 0;
  let startY = 0;
  let offsetX = 0;
  let offsetY = 0;

  refs.floatingR.addEventListener('pointerdown', (event) => {
    if (state.assist || state.floatingR.frozen) return;
    dragging = true;
    const rect = refs.floatingR.getBoundingClientRect();
    startX = event.clientX;
    startY = event.clientY;
    offsetX = startX - rect.left;
    offsetY = startY - rect.top;
    refs.floatingR.setPointerCapture(event.pointerId);
  });

  refs.floatingR.addEventListener('pointermove', (event) => {
    if (!dragging || state.assist || state.floatingR.frozen) return;
    setFloatingButtonPosition(event.clientX - offsetX, event.clientY - offsetY);
  });

  refs.floatingR.addEventListener('pointerup', () => {
    dragging = false;
  });

  refs.floatingR.addEventListener('pointerleave', () => {
    dragging = false;
  });

  refs.floatingR.addEventListener('click', () => {
    if (!dragging) {
      showRPanel();
    }
  });
}

function bindEvents() {
  document.querySelectorAll('[data-launch]').forEach((button) => {
    button.addEventListener('click', () => openGame(button.dataset.launch));
  });

  document.querySelectorAll('.color-swatch').forEach((swatch) => {
    swatch.addEventListener('click', () => setColor(swatch.dataset.color));
  });

  refs.assistToggle.addEventListener('change', syncAssistState);
  refs.headshot.addEventListener('input', (event) => {
    state.headshot = Number(event.target.value);
    refs.headshotValue.textContent = `${state.headshot}%`;
    setStatus(`HEADSHOT: ${state.headshot}%`);
    render();
  });

  refs.buttonSize.addEventListener('input', (event) => {
    state.size = Number(event.target.value);
    refs.buttonSizeValue.textContent = `${state.size}%`;
    render();
  });

  refs.buttonOpacity.addEventListener('input', (event) => {
    state.opacity = Number(event.target.value);
    refs.buttonOpacityValue.textContent = `${state.opacity}%`;
    render();
  });

  refs.crossSize.addEventListener('input', (event) => {
    state.crossSize = Number(event.target.value);
    refs.crossSizeValue.textContent = `${state.crossSize}%`;
    render();
  });

  refs.crossOpacity.addEventListener('input', (event) => {
    state.crossOpacity = Number(event.target.value);
    refs.crossOpacityValue.textContent = `${state.crossOpacity}%`;
    render();
  });

  refs.floatingSize.addEventListener('input', setFloatingSizeFromInput);
  refs.floatingOpacity.addEventListener('input', setFloatingSizeFromInput);

  refs.generalSens.addEventListener('input', (event) => {
    state.generalSens = Number(event.target.value);
    refs.generalSensValue.textContent = `${state.generalSens}%`;
  });
  refs.redDot.addEventListener('input', (event) => {
    state.redDot = Number(event.target.value);
    refs.redDotValue.textContent = `${state.redDot}%`;
  });
  refs.scope2x.addEventListener('input', (event) => {
    state.scope2x = Number(event.target.value);
    refs.scope2xValue.textContent = `${state.scope2x}%`;
  });
  refs.scope4x.addEventListener('input', (event) => {
    state.scope4x = Number(event.target.value);
    refs.scope4xValue.textContent = `${state.scope4x}%`;
  });
  refs.sniper.addEventListener('input', (event) => {
    state.sniper = Number(event.target.value);
    refs.sniperValue.textContent = `${state.sniper}%`;
  });
  refs.freeLook.addEventListener('input', (event) => {
    state.freeLook = Number(event.target.value);
    refs.freeLookValue.textContent = `${state.freeLook}%`;
  });

  refs.saveSettings.addEventListener('click', () => {
    saveState();
    setStatus('Настройки сохранены');
  });

  refs.resetApp.addEventListener('click', resetState);

  refs.freezeAim.addEventListener('click', () => {
    state.bubbleFrozen = !state.bubbleFrozen;
    refs.freezeAim.textContent = state.bubbleFrozen ? 'РАЗМОРОЗИТЬ ПРИЦЕЛ' : 'ЗАМОРОЗИТЬ ПРИЦЕЛ';
    setStatus(state.bubbleFrozen ? 'Прицел заморожен' : 'Перемещение снова доступно');
    saveState();
  });

  refs.hideAim.addEventListener('click', () => {
    const isHidden = refs.crosshairCanvas.style.opacity === '0';
    refs.crosshairCanvas.style.opacity = isHidden ? '1' : '0';
    setStatus(isHidden ? 'Прицел показан' : 'Прицел скрыт');
  });

  refs.shrinkCrosshair.addEventListener('click', () => {
    state.crossSize = Math.max(10, state.crossSize - 5);
    refs.crossSize.value = state.crossSize;
    refs.crossSizeValue.textContent = `${state.crossSize}%`;
    render();
  });

  refs.growCrosshair.addEventListener('click', () => {
    state.crossSize = Math.min(100, state.crossSize + 5);
    refs.crossSize.value = state.crossSize;
    refs.crossSizeValue.textContent = `${state.crossSize}%`;
    render();
  });

  refs.freezeRButton.addEventListener('click', freezeRPanel);
  refs.closeRPanel.addEventListener('click', hideRPanel);

  document.querySelectorAll('.profile-button').forEach((button) => {
    button.addEventListener('click', () => updateProfile(button.dataset.profile));
  });

  attachFloatingRInteractions();
}

loadState();
bindEvents();
render();
setStatus('Готово');
