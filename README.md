# RICC Partners

Site institucional da RICC Partners.

## Estrutura

| Arquivo | O que é |
| --- | --- |
| `RICC Site v2.dc.html` | **O site publicado.** Versão atual, servida na raiz (`/`) via rewrite do `vercel.json`. |
| `RICC Site.dc.html` | Versão 1 do site, mantida como referência. |
| `RICC Mobile.html` | Pré-visualização do site v2 dentro de uma moldura de iPhone (390 × 844). |
| `RICC Manual de Marca.dc.html` | Manual de marca. |
| `RICC Marca - *.dc.html` | Estudos e variações de logotipo (veleiro, tipográfica, família, encaixe "Partners"). |
| `RICC Cenas.dc.html` | Estudos de cena/direção de arte. |
| `support.js` | Runtime do Claude Design. Interpreta o bloco `<x-dc>`, aplica o `<helmet>` e carrega React 18 + Babel via CDN. |
| `image-slot.js` | Componente de slot de imagem usado pelas telas. |
| `img/` | Mídia do site (fotos e `hero-video.mp4`). |

## Como rodar localmente

Os arquivos usam caminhos relativos, então basta servir a pasta por HTTP
(abrir com `file://` não funciona):

```bash
python3 -m http.server 8000
# depois: http://localhost:8000/RICC%20Site%20v2.dc.html
```

## Publicação

Deploy estático na Vercel, sem etapa de build. O `vercel.json` faz `/` servir
o `RICC Site v2.dc.html`, preservando o nome original do arquivo para que ele
continue editável no canvas do Claude Design.

O runtime busca React, ReactDOM e Babel em `unpkg.com` no carregamento da
página — o site depende desse CDN estar acessível para o visitante.
