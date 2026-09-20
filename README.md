Nama    : Dyah Zhafira Wibowo
NPM     : 2506623723
Kelas   : PBP E

### Deskripsi Proyek

Website portofolio pribadi berbasis Django. Fitur: halaman Profile, Experience, Project (beserta detail), dashboard admin untuk CRUD Experience dan Project (khusus staff), pencarian, dan data tersedia dalam JSON (`/api/experiences/`, `/api/projects/`).

### Setup Lokal

1. Clone repo dan masuk ke foldernya.
2. Buat dan aktifkan virtual environment: `python -m venv .venv`, lalu `.venv\Scripts\activate` (Windows) atau `source .venv/bin/activate`.
3. Install dependensi: `pip install -r requirements.txt`.
4. Jalankan migrasi: `python manage.py migrate`.
5. Buat akun admin: `python manage.py createsuperuser`.
6. Jalankan server: `python manage.py runserver`, lalu buka `http://localhost:8000/`.
7. Jalankan test: `python manage.py test main`.

Login admin di `/login/`, dashboard di `/admin-panel/`.

### Progres Mingguan

- Tugas 1: halaman statis HTML5 dan CSS3, deploy ke PWS.
- Tugas 2: model Experience dan Project, migrasi, halaman dinamis, halaman detail berbasis slug, unit test.
- Tugas 3: template `base.html`, ModelForm, CRUD Experience dan Project khusus staff, JSON API, autentikasi, pencarian.

### TUGAS 1
1. pada Tutorial dan tugas 1, Anda diberi kebebasan untuk menentukan website tampilan dari website portfolio Anda. Saat anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5, seperti `<section>`. `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan Anda?

-> Ya, saya menggunakan elemen-elemen tersebut untuk membagi bagian-bagian pada halaman tersebut sesuai dengan kebutuhannya. Misal, untuk `<section>`, saya gunakan untuk memisahkan per section, seperti about, experiences, projects, dan skills. Sedangkan `<article>` saya gunakan untuk konten yang bisa berdiri sendiri, seperti tiap tiap item yang ada pada timeline section experiences dan tiap project's card. Namun, saya tidak menggunakan `<aside>` karena tidak ada bagian di halaman ini yang sifatnya seperti konten pelengkap atau di luar alur utama, karena memang saya sendiri merancang agar portfolio saya hanya fokus menampilkan konten utama agar user tidak terdistraksi. Sehingga, untuk saat ini tidak perlu `<aside>`.

2. Ketika Anda mengatur CSS anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

-> Menurut saya, tantangan utamanya ada pada bagian section projects dan skills yang berisi banyak item, seperti card dengan jumlah yang bisa berubah-ubah. Nah, jika saya set jumlah kolom secara fix, maka tampilannya bisa rusak atau tidak responsive di layar kecil seperti mobile, sehingga saya menggunakan grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)), yang membuat jumlah kolom menyesuaikan secara otomatis dengan lebar layar. Selain itu, elemen seperti ukuran foto dan garis timeline juga saya kecilkan ukurannya agar pas di mobile dan tidak overflow.

3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portfolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

-> Karena saat ini website ini masih statis, sehingga saya harus menulis codingannya serta melakukan deploy ulang tiap update profile, projects, dan pengalaman lainnya. Sehingga, untuk ke depannya, saya ingin menambahkan fitur admin dan sistem database agar saya dapat melakukan CRUD untuk update portfolio saya.

### AI DISCLOSURE
Saya menggunakan AI untuk membantu pengerjaan tugas ini dengan scope sebagai berikut:
1. Referensi design: Untuk memudahkan penyesuaian design, sehingga saya menanyakan terkait tema, skema warna, layout, serta font yang cocok.
2. Penjelasan syntax yang belum saya pahami: saat saya kesulitan untuk mengetahui suatu syntax, seperti bagaimana caranya hover pada card, membuat layout grid yang menyesuaikan jumlah kolom, timeline garis garis yang menggunakan pseudo element, serta cara menerapkan fitur aksesibilitas (pada skip-to-content & prefers-reduced-motion), saya meminta untuk dijelaskan konsep dan contoh implementasinya. Setelah itu, saya menyesuaikan sendiri. Karena terdapat keterbatasan AI, yaitu saat di awal penentuan tema, walaupun saya mengajukan warna pastel, namun saya tetap mempertimbangkan aksesibilitas. Namun, AI menyarankan warna yang tidak kontras sesuai WCAG AA. Sehingga, di akhir saya memperbaikinya dengan menambahkan variasi warna (mungkin keterbatasan ini hanya dari segi UI/UX designnya saja).
3. Penulisan ulang konten: deskripsi project ditulis ulang oleh AI dalam bahasa Indonesia menyesuaikan dengan project portfolio yang sudah saya buat (hanya merapihkan tata bahasa dari portfolio saya yang sebelumnya, struktur dan isi tetap oleh saya).

### FITUR TAMBAHAN

Terdapat beberapa fitur aksesibilitas untuk UI/UX sebagai berikut:
1. Skip to content link: ketika tekan tombol tab, maka akan muncul link "lewati ke konten utama". Sebenarnya untuk saat ini fungsi fitur tersebut belum terlihat karena masih sederhana dan hanya punya 1 link navigasi. Namun, fitur ini tetap diterapkan untuk best practice pengembangan kedepannya.

2. Visible focus state: seluruh elemen, seperti link navbar, card skill, card project, dan card experience dapat dinavigasi menggunakan tab dan akan menampilan outline yang jelas.

3. prefers reduced motion: seluruh animasi hover pada card dapat otomatis nonaktif jika user mengaktifkan fitur reduce motion

4. Kontras warna WCAG AA: Sebenarnya fitur ini hanya berkaitan dengan color palette, untuk memastikan sesuai dengan standar kontras. 

### TUGAS 2
1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template

-> Jadi saat browser akses `/project/`, request tersebut akan masuk ke `portfolio/urls.py`. Nah, di file tersebut ada `path("", include("main.urls"))`. Sehingga, semua path dilempar ke `main/urls.py` (ini yang level app). Kemudian, di file tersebut ada path `project/` yang sesuai sama `name="show_project`. Django memanggil fungsi `show_project` di `main/views.py`. Di view ini aku ambil semua data lewat `Project.objects.all()` yang ada di model project. Kemudia, masukin ke context `project_list`, lalu `render(request, "project.html", context)`. Terakhir, nantinya template buka `project.html` dan loop untuk tiap project dari `{% for project in project_list %}` dan tiap project.title, project.description, dll akan diganti oleh data dari database dan kalau project_list kosong template bakal masuk ke kondisi %empty%. Selain halaman ini, ada juga halaman detail per project yang alurnya mirip, namun terdapat slug untuk url nya.

2. Mengapa data untuk bagian portfolio baru sebaiknya disimpan pada model dan tidak di tulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

-> Kalau datanya di hardcode di HTML seperti sebelumnya, maka dari sisi developer, tiap kita akan menambah/edit/hapus atau CRUD, maka harus mengubah ke template secara langsung kemudian harus berulang kali deploy tiap kali dilakukan perubahan, sehingga rawan bug juga. Oleh karena itu, jika data berada di model, maka data akan terpisah dari tampilan sesuai MVT dan developer juga bisa ubah data secara langsung. Kalau dalam kasus ini, maka dapat diubah melalui Django shell dan untuk kedepannya dapat menggunakan admin panel tanp harus menyentuh kode template dan deploy berulang. Selain itu, code dan data jadi maintainable dan konsisten (minim typo), sehingga baik untuk scalability pengembangan lanjutannya.

3. Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut

-> makemigrations itu membandingkan model sekarang dengan history last migration kemudian generate file migrasi baru. Contohnya rancangan perubahan struktur tabel, tapi nantinya database belum benar benar keubah. Kalau migrate itu mengeksekusinya langsung ke database. Contohnya, saat saya nambahin field slug (unique, wajib) ke model project yang sudah ada 3 data, saat itu makemigrations sempat gagal karena semua baris lama kena default value yang sama (waktu itu saya isi default valuenya ""). Sehingga, melanggar constraint unique. Solusinya, nullable dulu field slugnya (agar migrasinya tidak perlu default dulu). Lalu, baru isi slug dengan data lama lewat shell. Kemudian, ubah lagi menjadi wajib dan jalanin makemigrations and migrate (udah aman).

### AI Disclosure (Tugas 2)
Selain scope yang sudah ada di Tugas 1. Di tugas 2 saya menggunakan ChatGPT & Claude dengan scope tambahan sebagai berikut:
1. Breakdown checklist tugas, di sini saya meminta AI untuk membantu struktur alur pengerjaan tugas, sehingga lebih terstruktur untuk mengerjakan step by step based on checklist yang diberikan.
2. Debugging migrasi & test, beberapa kali memang sempat terdapat error saat migrasi. Salah satunya seperti yang saya sebutkan sebelumnya, saya lupa bahwa saya sudah mengisi data project, sehingga terdapat bug ketika saya add field slug. Saya meminta AI untuk membantu debugging dan memberitahu juga cara debuggingnya agar saya juga bisa debugging sendiri. Namun, di tengah-tengah, justru claude yang membuat bug baru dari sarannya untuk menambahkan default value "". Sehingga, saya hapus migrasinya, dan mulai debugging dari awal dan mencobanya sendiri. Selain itu, saya minta untuk dijelskan penyebabnya dan selanjutnya saya eksekusi perbaikannya.
3. Referensi desain, karena terdapat page baru yang berbeda dengan page sebelumnya, sehingga saya meminta untuk diberikan referensi design agar konsisten. 

Notes: pada awal saya menggunakan claude code extension, saya lupa untuk memberikan constraint bahwa tidak boleh mengubah code secara langsung. Sehingga, ada beberapa bagian yang "inisiatif" dikerjakan claudenya, namun di akhir saya memberikan constraint tersebut dan undo perubahan yang dilakukan claude. Sehingga, peran claude di sini untuk bantu saya dalam debugging dan dieksekusi oleh saya.

Berikut link chatgpt: https://chatgpt.com/share/6aa66285-e0f4-83ec-9dd6-df711a5ac37a 

Karena saya tidak bisa mengirimkan link claudenya, berikut saya lampirkan prompt saat debugging:

```
Error-nya: UNIQUE constraint failed — soalnya waktu kamu pilih default "" (string kosong) buat 3 row yang udah ada, ketiganya jadi punya slug yang sama (""), padahal field-nya unique=True. Makanya gagal pas nulis ke database. Migrasinya kegagalan di tengah jalan (biasanya otomatis rollback di SQLite, jadi database kamu masih aman/utuh).

Cara benerinnya — pake pendekatan 2 tahap biar gak collide:

1. Hapus migrasi yang gagal tadi

rm main/migrations/0004_project_slug.py
2. Ubah model, slug sementara boleh kosong dulu
Di main/models.py:


slug = models.SlugField(unique=True, null=True, blank=True)
3. Generate & apply migrasi (harusnya lancar sekarang, karena null=True gak butuh default & SQLite ngebolehin banyak NULL walau field-nya unique)

python manage.py makemigrations
python manage.py migrate
4. Isi slug asli buat 3 project yang udah ada

python manage.py shell

from main.models import Project

Project.objects.filter(title__startswith="SignD").update(slug="signd")
Project.objects.filter(title__startswith="BEM UI").update(slug="bem-ui-spt")
Project.objects.filter(title__startswith="ClinicThinking").update(slug="clinicthinking")
5. Balikin model jadi wajib (gak nullable lagi)

slug = models.SlugField(unique=True)
6. Generate & apply migrasi lagi (kali ini aman, karena semua row udah punya slug unik)

python manage.py makemigrations
python manage.py migrate
Setelah itu lanjut ke langkah view/urls/template yang udah gw kasih sebelumnya. Kabarin kalau masih ada error di salah satu tahap ini.

c:\Users\USER\myportfolio\main\models.py
cara keluar dari shellnya gmn?
Ketik exit() terus enter, atau bisa juga Ctrl+Z lalu Enter (di Windows/PowerShell) buat keluar dari python manage.py shell.

kalo udah?
Lanjut ke langkah 5-6 dari instruksi sebelumnya:

5. Balikin model jadi wajib (gak nullable lagi) — di main/models.py:


slug = models.SlugField(unique=True)
(hapus null=True, blank=True)

6. Generate & apply migrasi lagi:


python manage.py makemigrations
python manage.py migrate
```

### FITUR TAMBAHAN

Terdapat fitur tambahan untuk tugas tambahan berupa detail page untuk masing masing experience yang ada.

### Tugas 3

1. Jelaskan mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!

-> Menurut saya, `ModelForm` lebih praktis karena form dapat langsung terhubung dengan model yang saya gunakan, yaitu `Experience`, sehingga field dan validasinya tidak perlu dibuat secara manual dari HTML. Selain itu melalui `ModelForm`, saya juga bisa menggunakan form yang sama untuk membuat dan mengupdate data experience. Sedangkan `{% csrf_token %}` digunakan untuk memastikan request dari form memang berasal dari website dan mencegah CSRF.

Pada bagian Experience, `ExperienceForm` dibuat langsung dari model `Experience`. Field, tipe input (select category, URL thumbnail, datetime-local tanggal), label, dan validasi (wajib diisi, max_length, pilihan yang valid) otomatis dari model, sehingga saya tidak perlu menulis HTML dan validasi satu per satu. Form yang sama juga dipakai untuk create dan update (dengan `instance=experience`). `{% csrf_token %}` wajib karena tanpa itu situs lain bisa membuat browser admin yang sedang login mengirim POST tanpa sepengetahuannya, misalnya menghapus atau mengubah Experience. Django menolak POST yang tidak membawa token valid, dan domain PWS didaftarkan di `CSRF_TRUSTED_ORIGINS`.

2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?

-> Menurut saya pribadi, JSON memang lebih sederhana dan mudah dibaca dibandingkan XML. Dalam portfolio ini juga, data `Project` dan `Experience` juga saya sediakan dalam bentuk JSON, sehingga lebih mudah untuk data delivery dari backend ke halaman web. Struktur JSON juga lebih ringkas karena menggunakan key value dan tidak membutuhkan tag seperti XML. JSON juga ga butuh tag pembuka dan penutup, lebih mudah dibaca, dan cepat di-parse. Pada portofolio ini, `/api/experiences/` return list objek berisi `model`, `pk`, dan `fields`, yang mudah dipakai frontend. XML lebih panjang dan butuh parser yang lebih berat.

3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?

-> Pada portfolio ini, saat `/api/experiences/?title=...` diakses, `urls.py` meneruskan request ke `get_experiences_json`. View mengambil `Experience` yang diurutkan berdasarkan `started_at`, memfilter judul lewat `filter_by_title` (di `services.py`), lalu `serializers.serialize("json", ...)` mengubahnya menjadi teks JSON `HttpResponse` dengan `content_type="application/json"`. Halaman `/experience/` memakai hasil yang sama, `show_experience` men-decode JSON itu, `serializers.deserialize` mengembalikannya menjadi objek `Experience`, lalu di-render ke `experience.html`. Serialization diperlukan karena queryset adalah objek Python (berisi UUID, datetime, dan koneksi database) yang tidak bisa dikirim lewat HTTP, sedangkan HTTP hanya membawa teks atau byte, jadi datanya harus diubah ke format standar yang bisa dibaca client mana pun.

### AI Disclosure (Tugas 3)
Tools: ChatGPT

Bagian yang dibantu:
- ChatGPT: breakdown checklist, penjelasan konsep (ModelForm, CRUD, authentication, authorization, JSON data delivery), diskusi batas akses admin, refactor `views.py` dan `services.py`, serta bantu debugging CRUD

Strategi prompting: saya meminta breakdown langkah dan penjelasan konsep dulu sebelum kode

Keterbatasan AI dan perbaikan manual:
- Potongan dashboard dari ChatGPT belum punya dasar autentikasi yang lengkap (login, redirect, izin staff), jadi saya debug sendiri dan mengatur `LOGIN_URL`, `LOGIN_REDIRECT_URL`, dan `LOGOUT_REDIRECT_URL`.
- AI kasih code `project_url` dan `project_image_url` di form padahal model di branch saya belum punya field itu, sehingga muncul `FieldError`. Sehingga, saya cek model dan sesuain form dengan model yang ada.
- Di akhir, terdapat sisa merge conflict yg menyebabkan `portfolio/urls.py` berisi route duplikat dan `<main>` bersarang. Sehingga, saya minta bantu dibersihkan dan memverifikasi hasilnya dengan test.

Link chat ChatGPT: https://chatgpt.com/share/6aae66bc-dc30-83ec-b191-515584aa9044

### FITUR TAMBAHAN

- Authentication and Admin Dashboard
- Menambahkan sistem login dan logout serta membatasi akses ke halaman admin dashboard
- Admin-Only CRUD Access
- Membatasi fitur Create, Update, dan Delete agar hanya dapat digunakan oleh pengguna yang memiliki akses admin

Dokumentasi akun admin secara lokal, jalankan:
python manage.py migrate
python manage.py createsuperuser

Untuk mencoba website yang sudah di-deploy, dapat menggunakan demo account berikut:
Username: demo
Password: demo123