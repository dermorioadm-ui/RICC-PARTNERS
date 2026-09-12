from pathlib import Path

p = Path('RICC Site v2.dc.html')
s = p.read_text(encoding='utf-8')

start = s.find("    const meterEl = document.querySelector('[data-meter]');")
end = s.find("\n\n    const KEEP =", start)
if start == -1 or end == -1:
    raise SystemExit('Mobile meter setup block not found; refusing unrelated edits.')

replacement = '''    const meterEl = document.querySelector('[data-meter]');
    const coarse = window.matchMedia('(pointer: coarse)').matches;
    let narrow = window.innerWidth < 760;
    this._dock = false;

    // Desktop: o círculo acompanha o mouse. Mobile: acompanha exatamente o dedo,
    // sem bloquear o gesto de scroll e sem ficar ancorado no rodapé/centro.
    let touchAt = 0;
    const placeTouchMeter = (x, y) => {
      if (!coarse || !meterEl) return;
      mx = x; my = y; touchAt = Date.now();
      meterEl.style.transform = 'translate3d(' + mx.toFixed(0) + 'px,' + my.toFixed(0) + 'px,0)';
    };
    const onTouchStart = e => {
      const t = e.touches && e.touches[0];
      if (t) placeTouchMeter(t.clientX, t.clientY);
    };
    const onTouchMove = e => {
      const t = e.touches && e.touches[0];
      if (t) placeTouchMeter(t.clientX, t.clientY);
    };
    const onPointerDown = e => {
      if (e.pointerType === 'touch' || e.pointerType === 'pen') placeTouchMeter(e.clientX, e.clientY);
    };
    const onPointerMove = e => {
      if ((e.pointerType === 'touch' || e.pointerType === 'pen') && e.buttons) placeTouchMeter(e.clientX, e.clientY);
    };
    window.addEventListener('touchstart', onTouchStart, { passive: true });
    window.addEventListener('touchmove', onTouchMove, { passive: true });
    window.addEventListener('pointerdown', onPointerDown, { passive: true });
    window.addEventListener('pointermove', onPointerMove, { passive: true });
    this._meterTouchOff = () => {
      window.removeEventListener('touchstart', onTouchStart);
      window.removeEventListener('touchmove', onTouchMove);
      window.removeEventListener('pointerdown', onPointerDown);
      window.removeEventListener('pointermove', onPointerMove);
    };

    // A barra de referência inferior continua independente do círculo SCROLL.
    let routeFill = null, routeLabel = null, routeTicks = [];'''
s = s[:start] + replacement + s[end:]

old = """      if (meter) {\n        if (!this._dock) meter.style.transform = 'translate3d(' + mx.toFixed(0) + 'px,' + my.toFixed(0) + 'px,0)';\n        if (Math.abs(y - (this._lastY || 0)) > 1) mAt = Date.now();\n        this._lastY = y;\n        // no celular o medidor fica ancorado no centro do rodape e cobria texto e foto:\n        // vira convite so na primeira tela, que e onde ele tem funcao\n        const inFold1 = fold1 && y >= fold1.offsetTop && y <= fold1.offsetTop + fold1.offsetHeight - vh + 4;\n        const cabe = !this._dock || inFold1;\n        meter.style.opacity = this._dock ? (cabe ? '1' : '0') : ((Date.now() - mAt < 900 && cabe) ? '1' : '0');\n      }"""
new = """      if (meter) {\n        meter.style.transform = 'translate3d(' + mx.toFixed(0) + 'px,' + my.toFixed(0) + 'px,0)';\n        if (Math.abs(y - (this._lastY || 0)) > 1) mAt = Date.now();\n        this._lastY = y;\n        const inFold1 = fold1 && y >= fold1.offsetTop && y <= fold1.offsetTop + fold1.offsetHeight - vh + 4;\n        if (coarse) {\n          // Só aparece junto do gesto e sempre na coordenada real do toque.\n          meter.style.opacity = (inFold1 && Date.now() - touchAt < 420) ? '1' : '0';\n        } else {\n          meter.style.opacity = (Date.now() - mAt < 900 && inFold1) ? '1' : '0';\n        }\n      }"""
if old not in s:
    raise SystemExit('Meter tick block not found; refusing unrelated edits.')
s = s.replace(old, new, 1)

old_unmount = """    if (this._resp) this._resp();\n    if (this._blobUrl) URL.revokeObjectURL(this._blobUrl);"""
new_unmount = """    if (this._resp) this._resp();\n    if (this._meterTouchOff) this._meterTouchOff();\n    if (this._blobUrl) URL.revokeObjectURL(this._blobUrl);"""
if old_unmount not in s:
    raise SystemExit('Unmount cleanup block not found.')
s = s.replace(old_unmount, new_unmount, 1)

p.write_text(s, encoding='utf-8')
