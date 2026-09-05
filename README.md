Nama    : Dyah Zhafira Wibowo
NPM     : 2506623723
Kelas   : PBP E

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

### FITUR TAMBAHAN

Terdapat beberapa fitur aksesibilitas untuk UI/UX sebagai berikut:
1. Skip to content link: ketika tekan tombol tab, maka akan muncul link "lewati ke konten utama". Sebenarnya untuk saat ini fungsi fitur tersebut belum terlihat karena masih sederhana dan hanya punya 1 link navigasi. Namun, fitur ini tetap diterapkan untuk best practice pengembangan kedepannya.

2. Visible focus state: seluruh elemen, seperti link navbar, card skill, card project, dan card experience dapat dinavigasi menggunakan tab dan akan menampilan outline yang jelas.

3. prefers reduced motion: seluruh animasi hover pada card dapat otomatis nonaktif jika user mengaktifkan fitur reduce motion

4. Kontras warna WCAG AA: Sebenarnya fitur ini hanya berkaitan dengan color palette, untuk memastikan sesuai dengan standar kontras. 