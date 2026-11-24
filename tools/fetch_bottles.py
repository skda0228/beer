"""baijiu/bottles.tsv 의 병 사진을 내려받아 baijiu/assets/bottles/<id>.webp 로 저장한다.
해당 이미지 서버에 접속이 허용된 환경에서 손으로 실행한다 (Pillow 필요).
결과는 표준 출력으로 낸다. 이미 있는 파일은 건너뛴다."""
import io, os, urllib.request
from PIL import Image

OUT = 'baijiu/assets/bottles'
os.makedirs(OUT, exist_ok=True)
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')
for line in open('baijiu/bottles.tsv', encoding='utf-8'):
    if line.startswith('#') or not line.strip():
        continue
    bid, name, url, ref = line.rstrip('\n').split('\t')
    path = f'{OUT}/{bid}.webp'
    if os.path.exists(path):
        print(f'{bid}\tkept'); continue
    try:
        origin = '/'.join(ref.split('/')[:3]) + '/'
        req = urllib.request.Request(url, headers={
            'User-Agent': UA, 'Referer': origin, 'Accept': 'image/webp,image/*,*/*'})
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read()
        im = Image.open(io.BytesIO(raw)); im.load()
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA')
            bg = Image.new('RGB', im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1]); im = bg
        else:
            im = im.convert('RGB')
        im.thumbnail((640, 640), Image.LANCZOS)
        im.save(path, 'WEBP', quality=82, method=6)
        print(f'{bid}\tok\t{im.size[0]}x{im.size[1]}\t{os.path.getsize(path)} bytes\t{name}')
    except Exception as e:
        print(f'{bid}\tFAIL\t{type(e).__name__}: {str(e)[:140]}\t{name}')
