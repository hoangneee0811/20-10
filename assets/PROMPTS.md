# HƯỚNG DẪN TẠO VÀ XỬ LÝ TÀI NGUYÊN ẢNH HOA

Tài liệu này chứa toàn bộ prompt chi tiết dùng để tạo bộ ảnh hoa giấy pastel (paper-craft rose illustration) cho ứng dụng thiệp 20/10 `garden.html`.

---

## 1. Hướng dẫn quy trình
1. Dùng mô hình tạo ảnh (Midjourney, DALL-E 3, Flux, hoặc Imagen) với tỷ lệ `1:1` (độ phân giải tối thiểu `1024x1024`).
2. Lưu các ảnh tạo được vào thư mục `assets/raw/` dưới định dạng PNG hoặc JPG với **đúng tên file** được quy định bên dưới (ví dụ: `hero.png`, `pink-01.png`, `bud-coral-01.png`,...).
3. Chạy lệnh xử lý tự động:
   ```bash
   python tools/process_assets.py
   ```
4. Script sẽ tự động:
   - Tách nền xám `#808080` bằng thuật toán Connected Components.
   - Khử viền xám (de-fringing) và làm mượt biên alpha (feathering 1px).
   - Cắt sát viền (trim) và chừa 3% đệm trong suốt.
   - Resize về đúng kích thước chuẩn (Hero: 1024, Hoa thường: 512, Nụ: 256, Cánh: 128).
   - Xuất định dạng WebP có alpha vào `assets/flowers/`.

---

## 2. Danh sách Prompt cho từng ảnh

### A. Hoa chủ đạo (Hero Flower) — 1024x1024
- **Tên file raw:** `assets/raw/hero.png`
- **Output:** `assets/flowers/hero.webp`
```
A single lush layered paper rose flower head, viewed from slightly above (about 20 degrees tilt), soft pastel pink (#f4a9bb), many overlapping rounded scalloped petals spiraling softly into a tight center, delicate handcrafted paper texture, soft shadows between petals, gentle gradient from deeper tone at the base of each petal to lighter tone at the edge, clean pastel illustration style, perfectly round silhouette, centered with 8% margin, no stem, no leaves, no text, no watermark, isolated on a flat uniform #808080 gray background, no cast shadow on the background, square, 1024x1024
```

---

### B. Nhóm hoa hồng phấn nhạt (Soft Pastel Pink) — 512x512
- **`assets/raw/pink-01.png`**
```
A single lush layered paper rose flower head, viewed from slightly above (about 15 degrees tilt), soft pastel baby pink (#f7b2c2), many overlapping rounded scalloped petals spiraling softly into a tight spiral center, delicate handcrafted paper texture, soft shadows between petals, gentle gradient from deeper pink at petal base to very pale blush pink at edge, clean pastel illustration style, perfectly round silhouette, centered with 8% margin, no stem, no leaves, no text, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

- **`assets/raw/pink-02.png`**
```
A single layered paper cabbage rose flower head, top-down view, delicate blush pink (#f4a8b8), ruffled wavy paper petal edges layered in concentric circles, tight rosette center, handcrafted origami crepe paper feel, soft ambient shadows, clean pastel style, round silhouette, centered, no stem, no leaves, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

- **`assets/raw/pink-03.png`**
```
A single blossoming layered paper rose flower head, slight angle view, warm powdered pink (#f5a3b5), multiple scalloped tiers of curved paper petals, spiral core, handcrafted layered paper relief, subtle paper grain, clean soft lighting, round silhouette, centered, no stem, no leaves, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

---

### C. Nhóm hoa hồng đậm / cánh sen (Deeper Rose Pink) — 512x512
- **`assets/raw/rose-01.png`**
```
A single lush layered paper rose flower head, viewed from slightly above, deeper rose pink (#e8708d) with magenta undertones, many overlapping rounded scalloped petals spiraling into a rich center, delicate paper craft texture, soft depth shadows between petal tiers, clean pastel illustration style, round silhouette, centered with 8% margin, no stem, no leaves, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

- **`assets/raw/rose-02.png`**
```
A single English garden layered paper rose, top-down view, vibrant rose coral pink (#e26382), concentric tiers of curled paper petals, tight swirl center, delicate paper texture, soft inner shadows, clean pastel illustration style, round silhouette, centered, no stem, no leaves, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

---

### D. Nhóm hoa cam đào (Peach Orange) — 512x512
- **`assets/raw/peach-01.png`**
```
A single lush layered paper rose flower head, viewed from slightly above, warm peach orange (#f8bd96) fading to soft apricot cream at the petal edges, many overlapping rounded scalloped petals, tight spiral center, handcrafted paper texture, soft dimensional shadows, clean pastel style, round silhouette, centered, no stem, no leaves, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

- **`assets/raw/peach-02.png`**
```
A single layered paper cabbage rose, top-down angle, soft pastel apricot peach (#fbc3a1), concentric ruffled petal rings, delicate quilled paper fold center, soft gradient lighting, clean illustration style, round silhouette, centered, no stem, no leaves, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

- **`assets/raw/peach-03.png`**
```
A single layered paper rose flower head, soft warm peach coral (#f6b088), multiple tiers of curved cupped paper petals spiraling into a neat center, fine papercraft texture, soft shadows, round silhouette, centered, no stem, no leaves, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

---

### E. Nhóm hoa xanh mint nhạt (Pale Mint Green) — 512x512
- **`assets/raw/mint-01.png`**
```
A single lush layered paper rose flower head, viewed from slightly above, pale mint green (#bfe3b0) with soft sage undertones, overlapping rounded scalloped paper petals, tight rosette center, handcrafted papercraft texture, delicate shading between layers, clean pastel style, round silhouette, centered, no stem, no leaves, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

- **`assets/raw/mint-02.png`**
```
A single layered paper garden rose, top-down view, soft pastel sage mint (#c6e7b8), concentric tiers of paper petals, delicate spiral core, handcrafted layered paper art, soft ambient lighting, round silhouette, centered, no stem, no leaves, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

---

### F. Nhóm hoa xanh dương nhạt (Pale Sky Blue) — 512x512
- **`assets/raw/blue-01.png`**
```
A single lush layered paper rose flower head, viewed from slightly above, pale sky blue (#a9cdee) fading to soft baby blue at the petal tips, overlapping rounded scalloped petals, tight spiral center, handcrafted paper texture, soft dimensional shadows, clean pastel style, round silhouette, centered, no stem, no leaves, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

- **`assets/raw/blue-02.png`**
```
A single layered paper cabbage rose, top-down view, soft cornflower pastel blue (#b3d4f0), concentric tiers of curled paper petals, delicate spiral rosette core, handcrafted paper art style, round silhouette, centered, no stem, no leaves, isolated on a flat uniform #808080 gray background, square, 1024x1024
```

---

### G. Nhóm hoa trắng kem sáng (Bright Ivory White) — 512x512
> **Lưu ý đặc biệt cho hoa trắng kem**: Không tạo trên nền xám #808080 để tránh lẫn màu viền cánh hoa. Bắt buộc tạo trên **nền tối tương phản** (`#2f3a40`) để tách nền chuẩn xác và giữ nguyên độ sáng trong trẻo của cánh hoa.

- **`assets/raw/ivory-01.png`**
```
A single lush layered paper rose flower head, viewed from slightly above, bright ivory white (#fffaf5) with very subtle soft warm cream undertones (clean luminous petals, not beige or gray), overlapping scalloped petals, tight spiral center, delicate paper texture, soft gentle depth shadows, clean pastel style, round silhouette, centered with 8% margin, no stem, no leaves, isolated on a flat uniform dark contrasting #2f3a40 charcoal background, no cast shadow, square, 1024x1024
```

- **`assets/raw/ivory-02.png`**
```
A single layered paper garden rose, top-down view, luminous clean ivory white (#fdfbf7), concentric tiers of paper petals, delicate spiral center fold, handcrafted paper relief, subtle warm glow, round silhouette, centered with 8% margin, no stem, no leaves, isolated on a flat uniform dark contrasting #2f3a40 charcoal background, no cast shadow, square, 1024x1024
```

---

### H. Nhóm nụ hoa (Rose Buds) — 256x256
- **`assets/raw/bud-pink-01.png`**
```
A single closed rose bud seen from the side, tapered teardrop flame shape, two-tone soft pastel pink at the top blending into creamy white at the base, small delicate green sepals at the bottom, handcrafted paper-craft pastel illustration style, no stem, no text, isolated on a flat uniform #808080 gray background, centered, square, 512x512
```

- **`assets/raw/bud-coral-01.png`**
```
A single closed rose bud seen from the side, elegant tapered teardrop shape, two-tone vibrant coral pink (#e8657f) at top fading to clean warm white at bottom, two small pointed green sepals clasping the base, paper-craft pastel illustration style, no stem, no text, isolated on a flat uniform #808080 gray background, centered, square, 512x512
```

- **`assets/raw/bud-white-01.png`**
```
A single closed rose bud seen from the side, slender teardrop shape, soft pastel sky blue and ivory white two-tone petals, small green sepals at the bottom, paper-craft pastel illustration style, no stem, no text, isolated on a flat uniform #808080 gray background, centered, square, 512x512
```

---

### I. Nhóm cánh hoa rơi (Fallen Petals) — 128x128
- **`assets/raw/petal-01.png`**
```
A single rose petal, slightly curved cupped shell shape, soft pastel pink with subtle paper texture, rounded top rim and narrower tapered base, paper-craft illustration style, no text, isolated on a flat uniform #808080 gray background, centered, square, 256x256
```

- **`assets/raw/petal-02.png`**
```
A single rose petal, gently curled and undulating, warm pastel peach pink, handcrafted paper texture, delicate shading, clean illustration style, no text, isolated on a flat uniform #808080 gray background, centered, square, 256x256
```
