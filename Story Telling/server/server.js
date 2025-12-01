import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import multer from 'multer';
import axios from 'axios';

const app = express();
const upload = multer({ storage: multer.memoryStorage() });
app.use(cors());
app.use(express.json({ limit: '2mb' }));
app.use(express.static('public'));

function getBearer(req) {
// Authorization precedence: header "Authorization: Bearer <token>" or query ?token=
const h = req.headers.authorization || '';
if (h.toLowerCase().startsWith('bearer ')) return h.slice(7).trim();
if (req.query.token) return String(req.query.token);
if (process.env.HF_TOKEN) return process.env.HF_TOKEN;
return null;
}

function hfHeaders(token) {
return {
Authorization: `Bearer ${token}`,
'Content-Type': 'application/json'
};
}

// Generic text generation proxy
app.post('/api/text-generate', async (req, res) => {
try {
const token = getBearer(req);
const { model = 'microsoft/DialoGPT-medium', inputs, parameters = {} } = req.body;

text
if (!token) {
  // Offline demo mode
  return res.json({
    demo: true,
    model,
    outputs: [
      { generated_text: `[DEMO] ${String(inputs).slice(0, 160)} ...` }
    ]
  });
}

const url = `https://api-inference.huggingface.co/models/${encodeURIComponent(model)}`;
const resp = await axios.post(url, { inputs, parameters }, { headers: hfHeaders(token), timeout: 60_000 });
return res.json({ demo: false, model, outputs: resp.data });
} catch (err) {
const msg = err?.response?.data || err?.message || 'Unknown error';
return res.status(500).json({ error: 'TEXT_GENERATE_FAILED', detail: msg });
}
});

// Text-to-image (Stable Diffusion-like). Returns base64 PNG.
app.post('/api/text-to-image', async (req, res) => {
try {
const token = getBearer(req);
const {
model = 'stable-diffusion-v1-5/stable-diffusion-v1-5',
prompt = 'a cat reading a book',
num_inference_steps = 20,
guidance_scale = 7.5,
width = 512,
height = 512,
seed = undefined
} = req.body;

text
if (!token) {
  // Offline demo mode: return placeholder
  return res.json({
    demo: true,
    model,
    image_base64: null,
    note: 'Demo mode: provide HF token to generate real images.'
  });
}

const url = `https://api-inference.huggingface.co/models/${encodeURIComponent(model)}`;
const response = await axios.post(
  url,
  { inputs: prompt, parameters: { num_inference_steps, guidance_scale, width, height, seed } },
  {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: 'image/png',
      'Content-Type': 'application/json'
    },
    responseType: 'arraybuffer',
    timeout: 120_000
  }
);

const b64 = Buffer.from(response.data).toString('base64');
return res.json({ demo: false, model, image_base64: `data:image/png;base64,${b64}` });
} catch (err) {
const msg = err?.response?.data || err?.message || 'Unknown error';
return res.status(500).json({ error: 'TEXT_TO_IMAGE_FAILED', detail: msg });
}
});

// Image-to-caption. Accepts multipart form "image".
app.post('/api/image-to-caption', upload.single('image'), async (req, res) => {
try {
const token = getBearer(req);
const model = req.body.model || 'nlpconnect/vit-gpt2-image-captioning'; // common public example

text
if (!token) {
  // Offline demo mode
  return res.json({
    demo: true,
    model,
    caption: 'A placeholder caption for a demo image.'
  });
}

if (!req.file) {
  return res.status(400).json({ error: 'NO_IMAGE', detail: 'Upload image as form-data field "image".' });
}

const url = `https://api-inference.huggingface.co/models/${encodeURIComponent(model)}`;
const resp = await axios.post(url, req.file.buffer, {
  headers: {
    Authorization: `Bearer ${token}`,
    Accept: 'application/json',
    'Content-Type': req.file.mimetype || 'application/octet-stream'
  },
  timeout: 90_000
});

// Many image-to-text models return array of {generated_text}
const data = resp.data;
let caption = 'No caption';
if (Array.isArray(data) && data?.generated_text) caption = data.generated_text;
else if (data?.generated_text) caption = data.generated_text;

return res.json({ demo: false, model, caption });
} catch (err) {
const msg = err?.response?.data || err?.message || 'Unknown error';
return res.status(500).json({ error: 'IMAGE_TO_CAPTION_FAILED', detail: msg });
}
});

// Health
app.get('/api/health', (_req, res) => res.json({ ok: true, mode: getBearer(_req) ? 'online' : 'demo' }));

const PORT = process.env.PORT || 5173;
app.listen(PORT, () => console.log('Gen AI Demo Hub running on http://localhost:${PORT}'));