// --- 1. DỮ LIỆU HARDCODE (Mock Data) ĐÃ FIX ẢNH ---
let artists = [
    { id: 301, name: "Sơn Tùng M-TP", img: "https://ui-avatars.com/api/?name=Son+Tung+M+TP&background=db2777&color=fff&size=300" },
    { id: 302, name: "Soobin Hoàng Sơn", img: "https://ui-avatars.com/api/?name=Soobin+Hoang+Son&background=2563eb&color=fff&size=300" },
    { id: 303, name: "Vũ.", img: "https://ui-avatars.com/api/?name=Vu&background=059669&color=fff&size=300" },
    { id: 304, name: "tlinh", img: "https://ui-avatars.com/api/?name=tlinh&background=c026d3&color=fff&size=300" },
    { id: 305, name: "Binz", img: "https://ui-avatars.com/api/?name=Binz&background=dc2626&color=fff&size=300" },
    { id: 306, name: "Đen Vâu", img: "https://ui-avatars.com/api/?name=Den+Vau&background=4b5563&color=fff&size=300" },
    { id: 307, name: "Hoàng Thùy Linh", img: "https://ui-avatars.com/api/?name=Hoang+Thuy+Linh&background=ea580c&color=fff&size=300" },
    { id: 308, name: "Phương Ly", img: "https://ui-avatars.com/api/?name=Phuong+Ly&background=ec4899&color=fff&size=300" },
    { id: 309, name: "MCK", img: "https://ui-avatars.com/api/?name=MCK&background=000000&color=fff&size=300" },
    { id: 310, name: "Wxrdie", img: "https://ui-avatars.com/api/?name=Wxrdie&background=7c3aed&color=fff&size=300" }
];

let songs = [
    { id: 11, title: "Chạy Ngay Đi", artist: "Sơn Tùng M-TP", genre: "Pop, R&B", img: "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/15/13/cb/1513cb0b-c5a9-ac85-32ec-907ecfc98c8e/23UM1IM10668.rgb.jpg/500x500bb.jpg", url: "https://www.bensound.com/bensound-music/bensound-energy.mp3", artistId: 301 },
    { id: 12, title: "Phía Sau Một Cô Gái", artist: "Soobin Hoàng Sơn", genre: "Pop", img: "https://ui-avatars.com/api/?name=Phia+Sau+Mot+Co+Gai&background=random&color=fff&size=300", url: "https://www.bensound.com/bensound-music/bensound-creativeminds.mp3", artistId: 302 },
    { id: 13, title: "Bước Qua Nhau", artist: "Vũ.", genre: "Indie Pop", img: "https://ui-avatars.com/api/?name=Buoc+Qua+Nhau&background=random&color=fff&size=300", url: "https://www.bensound.com/bensound-music/bensound-acousticbreeze.mp3", artistId: 303 },
    { id: 14, title: "Gái Độc Thân", artist: "tlinh", genre: "Rap, R&B", img: "https://ui-avatars.com/api/?name=Gai+Doc+Than&background=random&color=fff&size=300", url: "https://www.bensound.com/bensound-music/bensound-sunny.mp3", artistId: 304 },
    { id: 15, title: "Bigcityboi", artist: "Binz", genre: "Rap", img: "https://ui-avatars.com/api/?name=Bigcityboi&background=random&color=fff&size=300", url: "https://www.bensound.com/bensound-music/bensound-epic.mp3", artistId: 305 },
    { id: 16, title: "Đi Về Nhà", artist: "Đen Vâu", genre: "Rap, Indie", img: "https://ui-avatars.com/api/?name=Di+Ve+Nha&background=random&color=fff&size=300", url: "https://www.bensound.com/bensound-music/bensound-energy.mp3", artistId: 306 },
    { id: 17, title: "See Tình", artist: "Hoàng Thùy Linh", genre: "Pop, Dance", img: "https://ui-avatars.com/api/?name=See+Tinh&background=random&color=fff&size=300", url: "https://www.bensound.com/bensound-music/bensound-creativeminds.mp3", artistId: 307 },
    { id: 18, title: "Thích Thích", artist: "Phương Ly", genre: "Pop", img: "https://ui-avatars.com/api/?name=Thich+Thich&background=random&color=fff&size=300", url: "https://www.bensound.com/bensound-music/bensound-sunny.mp3", artistId: 308 },
    { id: 19, title: "Chìm Sâu", artist: "MCK", genre: "R&B, Rap", img: "https://ui-avatars.com/api/?name=Chim+Sau&background=random&color=fff&size=300", url: "https://www.bensound.com/bensound-music/bensound-epic.mp3", artistId: 309 },
    { id: 20, title: "Harder", artist: "Wxrdie", genre: "Rap", img: "https://ui-avatars.com/api/?name=Harder&background=random&color=fff&size=300", url: "https://www.bensound.com/bensound-music/bensound-epic.mp3", artistId: 310 },
    
    // Nhạc nền mặc định
    { id: 1, title: "Energy Rock", artist: "Bensound", genre: "Rock", img: "https://ui-avatars.com/api/?name=Energy+Rock&background=random&color=fff&size=300", url: "https://www.bensound.com/bensound-music/bensound-energy.mp3", artistId: null },
    { id: 3, title: "Acoustic Breeze", artist: "Bensound", genre: "Acoustic", img: "https://ui-avatars.com/api/?name=Acoustic+Breeze&background=random&color=fff&size=300", url: "https://www.bensound.com/bensound-music/bensound-acousticbreeze.mp3", artistId: null }
];

let playlists = JSON.parse(localStorage.getItem('ai_music_default_playlists')) || [
    { id: 101, name: "Lofi Chill", songs: [1, 13] }
];

function saveDefaultPlaylists() {
    localStorage.setItem('ai_music_default_playlists', JSON.stringify(playlists));
}

let customImages = JSON.parse(localStorage.getItem('ai_player_custom_images') || "{}");
function applyCustomImages() {
    artists.forEach(a => { if (customImages[`artist_${a.id}`]) a.img = customImages[`artist_${a.id}`]; });
    songs.forEach(s => { if (customImages[`song_${s.id}`]) s.img = customImages[`song_${s.id}`]; });
}
applyCustomImages();

let playQueue = [];
let queueHistory = [];
let isShuffle = false;
let repeatMode = 0;
let currentPlaylistContext = [];

function getVisibleSongs() {
    return [...songs];
}

function findSongById(id) { return getVisibleSongs().find(song => song.id === id); }
function getPlaylistSource() { return playlists; }

function updateAuthUI() {
    // Luôn luôn ở trạng thái "Công khai" - gỡ bỏ logic check User
    const uploadButton = document.getElementById('upload-button');
    if (uploadButton) { uploadButton.disabled = false; uploadButton.title = 'Tải nhạc lên hệ thống'; }
    renderPlaylistsSidebar();
}

// Giả lập hàm cho Upload khi không có Backend (sẽ thay bằng API ở Track 3)
window.attemptUpload = function() { 
    document.getElementById('upload-input').click(); 
};

function recordListening(song) {
    if (!song) return;
    // Tạm thời tắt ghi nhận sở thích người dùng cho v2.1 No-Auth
}

let currentEditType = null;
let currentEditId = null;

window.triggerImageUpload = function(type, id) {
    currentEditType = type;
    currentEditId = id;
    document.getElementById('custom-image-input').click();
}

document.getElementById('custom-image-input')?.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(event) {
        const base64Url = event.target.result;
        customImages[`${currentEditType}_${currentEditId}`] = base64Url;
        localStorage.setItem('ai_player_custom_images', JSON.stringify(customImages));
        applyCustomImages();
        
        if (currentEditType === 'artist' && document.getElementById('artist-view').style.display !== 'none') {
            document.getElementById('artist-view-img').src = base64Url;
            renderArtists(document.getElementById('search-input')?.value.trim() || "");
        } else if (currentEditType === 'song') {
            document.getElementById('detail-img').src = base64Url;
            if (currentSongId === currentEditId) document.getElementById('player-img').src = base64Url;
            renderSongs(document.getElementById('search-input')?.value.trim() || "");
            renderHabitAndTrendingSongs();
            if (document.getElementById('playlist-view').style.display === 'block') {
                viewPlaylist(parseInt(document.getElementById('current-playlist-id').value));
            }
        }
        showToast("Đã thay đổi ảnh!");
    };
    reader.readAsDataURL(file);
    e.target.value = "";
});

// Fallback ảnh cuối cùng nếu picsum chết
const IMAGE_FALLBACK_URL = 'https://via.placeholder.com/300?text=No+Image';
document.addEventListener('error', (event) => {
    const img = event.target;
    if (img.tagName === 'IMG' && !img.dataset.fallback) { img.dataset.fallback = 'true'; img.src = IMAGE_FALLBACK_URL; }
}, true);

// --- 2. BIẾN TOÀN CỤC & DOM ELEMENTS ---
const audioEl = document.getElementById('real-audio-player');
const playPauseIcon = document.getElementById('icon-play-pause');
const seekSlider = document.getElementById('seek-slider');
const timeCurrentEl = document.getElementById('time-current');
const timeTotalEl = document.getElementById('time-total');
const volumeSlider = document.getElementById('volume-slider');

let isPlaying = false;
let currentSongId = null;

const themeToggle = document.getElementById('theme-toggle');
if (themeToggle) {
    themeToggle.addEventListener('change', (e) => {
        if (e.target.checked) document.body.classList.add('light-theme');
        else document.body.classList.remove('light-theme');
    });
}

// --- 3. ĐỔ DỮ LIỆU LÊN GIAO DIỆN ---
const artistsGrid = document.getElementById('artists-grid');
const mainList = document.getElementById('library-songs-list');
updateAuthUI();

function renderArtists(filterText = "") {
    artistsGrid.innerHTML = '';
    const filtered = artists.filter(a => a.name.toLowerCase().includes(filterText.toLowerCase()));
    
    filtered.forEach(a => {
        const card = document.createElement('div'); card.className = 'music-card'; card.style.textAlign = 'center'; card.onclick = () => viewArtist(a.id);
        card.innerHTML = `
            <div class="card-image-container" style="display: flex; justify-content: center; box-shadow: none; background: transparent;">
                <img src="${a.img}" alt="${a.name}" style="width: 130px; height: 130px; border-radius: 50%; object-fit: cover; margin-bottom: 8px;">
            </div>
            <h3 class="card-title">${a.name}</h3><p class="card-desc">Nghệ sĩ</p>
        `;
        artistsGrid.appendChild(card);
    });
    
    document.getElementById('artists-dashboard-section').style.display = filtered.length === 0 ? 'none' : 'block';
}

function renderSongs(filterText = "") {
    if (!mainList) return;
    mainList.innerHTML = '';
    const visibleSongs = getVisibleSongs();
    const filtered = visibleSongs.filter(s => s.title.toLowerCase().includes(filterText.toLowerCase()) || s.artist.toLowerCase().includes(filterText.toLowerCase()));

    if (document.getElementById('library-count')) document.getElementById('library-count').textContent = filtered.length;
    if (document.getElementById('library-recent')) document.getElementById('library-recent').textContent = filtered[0]?.title || 'Chưa có';

    if (filtered.length === 0) { mainList.innerHTML = '<li style="color:var(--text-subdued); padding:20px 0;">Không tìm thấy bài hát nào.</li>'; return; }

    filtered.forEach((songObj) => {
        const li = document.createElement('li'); li.className = 'song-list-item'; li.id = `song-list-item-${songObj.id}`;
        li.style = "display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--bg-hover); transition: background-color 0.2s;";
        li.onmouseenter = () => { if(currentSongId !== songObj.id) li.style.backgroundColor = "var(--bg-highlight)"; };
        li.onmouseleave = () => { if(currentSongId !== songObj.id) li.style.backgroundColor = "transparent"; };

        li.innerHTML = `
            <div style="width: 40px; text-align: center;">
                <button onclick="playSelectedSong(${songObj.id}, event)" style="background: transparent; border: none; color: var(--text-base); font-size: 14px; cursor: pointer;" title="Phát"><i class="fa-solid fa-play"></i></button>
            </div>
            <div style="flex: 1; display: flex; align-items: center; gap: 12px;">
                <img src="${songObj.img}" alt="img" style="width: 40px; height: 40px; border-radius: 4px; object-fit: cover;">
                <div style="display:flex; flex-direction: column;">
                    <span style="font-weight: 600; color: var(--text-base); cursor: pointer;" onclick="playSelectedSong(${songObj.id})">${songObj.title}</span>
                </div>
            </div>
            <div style="width: 150px; color: var(--text-subdued); font-size: 13px;">${songObj.artist}</div>
            <div style="width: 150px; color: var(--text-subdued); font-size: 13px;">${songObj.genre}</div>
            <div style="width: 80px; text-align: center; color: var(--text-subdued);">3:45</div>
            <div style="width: 120px; text-align: center; display: flex; justify-content: center; gap: 16px;">
                <button title="Chi tiết" onclick="openSongDetail(${songObj.id}, event)" style="background: transparent; color: var(--text-subdued); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-circle-info"></i></button>
                <button title="Thêm Playlist" onclick="openAddToPlaylistModal(${songObj.id}, event)" style="background: transparent; color: var(--text-subdued); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-plus"></i></button>
                <button title="Thêm Danh Sách Chờ" onclick="addToQueue(${songObj.id}, event)" style="background: transparent; color: var(--text-base); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-square-plus"></i></button>
            </div>
        `;
        mainList.appendChild(li);
    });
    if (currentSongId) updateHighlight(currentSongId);
}

window.handleSearch = function(e) {
    if (!e || !e.target) return;
    const term = e.target.value.toLowerCase().trim();
    const dropdown = document.getElementById('search-dropdown');
    const artistUl = document.getElementById('search-artist-result');
    const songUl = document.getElementById('search-song-result');

    if (!term) { dropdown.style.display = 'none'; goBackToHome(); renderArtists(); renderSongs(); return; }
    dropdown.style.display = 'block';

    const fArtists = artists.filter(a => a.name.toLowerCase().includes(term));
    artistUl.innerHTML = '';
    if (fArtists.length === 0) artistUl.innerHTML = '<span style="color:var(--text-subdued); font-size:13px;">Không tìm thấy.</span>';
    else {
        fArtists.slice(0, 4).forEach(a => {
            const li = document.createElement('li'); li.style = "display:flex; align-items:center; gap:10px; cursor:pointer; padding: 6px; border-radius: 4px; transition: background-color 0.2s;";
            li.onmouseenter = () => li.style.backgroundColor = "var(--bg-hover)"; li.onmouseleave = () => li.style.backgroundColor = "transparent";
            li.onclick = () => { dropdown.style.display = 'none'; document.getElementById('search-input').value = ''; viewArtist(a.id); };
            li.innerHTML = `<img src="${a.img}" style="width:36px; height:36px; border-radius:50%; object-fit:cover;"><span style="font-size:14px; font-weight:600; color:var(--text-base);">${a.name}</span>`;
            artistUl.appendChild(li);
        });
    }

    const fSongs = getVisibleSongs().filter(s => s.title.toLowerCase().includes(term) || s.artist.toLowerCase().includes(term));
    songUl.innerHTML = '';
    if (fSongs.length === 0) songUl.innerHTML = '<span style="color:var(--text-subdued); font-size:13px;">Không tìm thấy.</span>';
    else {
        fSongs.slice(0, 6).forEach(song => {
            const li = document.createElement('li'); li.style = "display:flex; align-items:center; gap:12px; cursor:pointer; padding: 6px; border-radius: 4px; transition: background-color 0.2s;";
            li.onmouseenter = () => li.style.backgroundColor = "var(--bg-hover)"; li.onmouseleave = () => li.style.backgroundColor = "transparent";
            li.onclick = (ev) => { dropdown.style.display = 'none'; playSelectedSong(song.id, ev); };
            li.innerHTML = `
                <img src="${song.img}" style="width:36px; height:36px; border-radius:4px; object-fit:cover;">
                <div style="display:flex; flex-direction:column;"><span style="font-size:14px; font-weight:600; color:var(--text-base); line-height: 1.2;">${song.title}</span><span style="font-size:12px; color:var(--text-subdued); margin-top:2px;">${song.artist}</span></div>
            `;
            songUl.appendChild(li);
        });
    }
    renderArtists(term); renderSongs(term);
}

document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('search-dropdown'); const searchBar = document.querySelector('.search-bar');
    if (dropdown && dropdown.style.display === 'block' && !dropdown.contains(e.target) && !searchBar.contains(e.target) && e.target.id !== 'search-input') { dropdown.style.display = 'none'; }
});

renderArtists(); renderSongs(); renderHabitAndTrendingSongs(); renderPlaylistsSidebar();

function renderHabitAndTrendingSongs() {
    const habitGrid = document.getElementById('habit-songs-grid'); const trendingGrid = document.getElementById('trending-songs-grid');
    if (!habitGrid || !trendingGrid) return;
    habitGrid.innerHTML = ''; trendingGrid.innerHTML = '';
    
    const visibleSongs = getVisibleSongs();
    if (!visibleSongs.length) return;

    let habitSongs = [...visibleSongs].sort(() => 0.5 - Math.random()).slice(0, 5);

    habitSongs.forEach(song => {
        const card = document.createElement('div'); card.className = 'music-card';
        card.innerHTML = `
            <div class="card-image-container"><img src="${song.img}" class="card-image" style="aspect-ratio: 1/1; object-fit: cover;"><button class="card-play-btn" onclick="playSelectedSong(${song.id}, event)"><i class="fa-solid fa-play"></i></button></div>
            <button class="card-add-btn" title="Chi tiết" onclick="openSongDetail(${song.id}, event)"><i class="fa-solid fa-circle-info"></i></button>
            <button class="card-queue-btn" title="Thêm danh sách chờ" onclick="addToQueue(${song.id}, event)"><i class="fa-solid fa-square-plus"></i></button>
            <h3 class="card-title">${song.title}</h3><p class="card-desc" style="font-size: 13px;">Gợi ý từ ${song.artist}</p>
        `;
        habitGrid.appendChild(card);
    });

    const trending = [...visibleSongs].sort(() => 0.5 - Math.random()).slice(0, 5);
    trending.forEach(song => {
        const card = document.createElement('div'); card.className = 'music-card';
        card.innerHTML = `
            <div class="card-image-container" style="position: relative;"><img src="${song.img}" class="card-image" style="aspect-ratio: 1/1; object-fit: cover;"><button class="card-play-btn" onclick="playSelectedSong(${song.id}, event)"><i class="fa-solid fa-play"></i></button><div style="position: absolute; top: 8px; left: 8px; background: #e74c3c; color: white; border-radius: 4px; padding: 4px 8px; font-size: 10px; font-weight: 800; text-transform: uppercase;">Top Xu Hướng</div></div>
            <button class="card-add-btn" title="Thêm Playlist" onclick="openAddToPlaylistModal(${song.id}, event)"><i class="fa-solid fa-plus"></i></button>
            <button class="card-queue-btn" title="Thêm danh sách chờ" onclick="addToQueue(${song.id}, event)"><i class="fa-solid fa-square-plus"></i></button>
            <h3 class="card-title">${song.title}</h3><p class="card-desc" style="font-size: 13px;">${song.artist} <span style="font-size: 11px; opacity: 0.8; color: var(--essential-positive);"><br>• ${Math.floor(Math.random()*4+1)}.${Math.floor(Math.random()*9)}M Lượt Nghe</span></p>
        `;
        trendingGrid.appendChild(card);
    });
}

function formatTime(seconds) { if (isNaN(seconds)) return "0:00"; const mins = Math.floor(seconds / 60); const secs = Math.floor(seconds % 60); return `${mins}:${secs < 10 ? '0' : ''}${secs}`; }

window.toggleShuffle = function() {
    isShuffle = !isShuffle;
    document.getElementById('btn-shuffle').classList.toggle('active', isShuffle);
    showToast(isShuffle ? "Bật trộn bài" : "Tắt trộn bài");
}

window.toggleRepeat = function() {
    repeatMode = (repeatMode + 1) % 3;
    const btn = document.getElementById('btn-repeat');
    if (repeatMode === 0) { btn.classList.remove('active'); btn.innerHTML = '<i class="fa-solid fa-repeat"></i>'; showToast("Tắt lặp lại"); }
    if (repeatMode === 1) { btn.classList.add('active'); btn.innerHTML = '<i class="fa-solid fa-repeat"></i>'; showToast("Lặp lại danh sách"); }
    if (repeatMode === 2) { btn.classList.add('active'); btn.innerHTML = '<i class="fa-solid fa-repeat" style="position:relative"><span style="position:absolute;font-size:9px;top:5px;left:7px;color:black">1</span></i>'; showToast("Lặp lại 1 bài"); }
}

window.playNext = function() {
    if (!currentSongId) return;
    queueHistory.push(currentSongId);
    if (queueHistory.length > 50) queueHistory.shift();

    if (playQueue.length > 0) {
        const nextId = playQueue.shift();
        const nextSong = findSongById(nextId);
        if (nextSong) {
            loadAndPlaySong(nextSong, false); 
            if (document.getElementById('queue-modal').classList.contains('active')) renderQueue();
            return;
        }
    }
    
    const context = currentPlaylistContext.length > 0 ? currentPlaylistContext : getVisibleSongs().map(s => s.id);
    if (context.length === 0) return;

    if (isShuffle) {
        let randId = context[Math.floor(Math.random() * context.length)];
        loadAndPlaySong(findSongById(randId), false);
    } else {
        const idx = context.indexOf(currentSongId);
        if (idx !== -1 && idx < context.length - 1) {
            loadAndPlaySong(findSongById(context[idx + 1]), false);
        } else if (repeatMode === 1) {
            if (context.length > 0) loadAndPlaySong(findSongById(context[0]), false);
        } else {
            audioEl.currentTime = 0; audioEl.pause(); isPlaying = false; playPauseIcon.className = 'fa-solid fa-play';
        }
    }
}

window.playPrevious = function() {
    if (audioEl.currentTime > 3) { audioEl.currentTime = 0; return; }
    if (queueHistory.length > 0) {
        const prevId = queueHistory.pop();
        if (currentSongId && !playQueue.includes(currentSongId)) playQueue.unshift(currentSongId);
        loadAndPlaySong(findSongById(prevId), false);
        if (document.getElementById('queue-modal').classList.contains('active')) renderQueue();
    } else {
        audioEl.currentTime = 0;
    }
}

function playSelectedSong(id, event) { 
    if (event) event.stopPropagation(); 
    const song = findSongById(id); 
    if (song) {
        currentPlaylistContext = getVisibleSongs().map(s => s.id); // Default root context
        loadAndPlaySong(song, true);
    }
}

function loadAndPlaySong(song, isManual = false) {
    if (isManual && currentSongId && currentSongId !== song.id) {
        queueHistory.push(currentSongId);
    }
    currentSongId = song.id;
    document.getElementById('player-img').src = song.img;
    document.getElementById('player-title').textContent = song.title; document.getElementById('player-artist').textContent = song.artist;
    audioEl.src = song.url; 
    
    const playPromise = audioEl.play();
    if (playPromise !== undefined) {
        playPromise.then(() => {
            isPlaying = true; playPauseIcon.className = 'fa-solid fa-pause';
        }).catch(err => {
            console.error("Audio playback error:", err);
            if (song.url.startsWith('blob:')) {
                showToast("File nhạc tải lên đã hết hạn phiên Local. Phục hồi phát bằng nhạc hệ thống.");
                song.url = "https://www.bensound.com/bensound-music/bensound-acousticbreeze.mp3";
                if (currentUser) saveAccounts(); // Keep fallback URL so they don't see error continuously
                audioEl.src = song.url;
                audioEl.play().then(() => {
                    isPlaying = true; playPauseIcon.className = 'fa-solid fa-pause';
                }).catch(e => console.log("Fallback failed:", e));
            } else {
                isPlaying = false; playPauseIcon.className = 'fa-solid fa-play';
            }
        });
    } else {
        isPlaying = true; playPauseIcon.className = 'fa-solid fa-pause';
    }

    updateHighlight(song.id); triggerAIFake(song.id); recordListening(song);
    
    if (seekSlider && seekSlider.value == 0 && audioEl.currentTime == 0) { seekSlider.style.background = '#4d4d4d'; }
}

function updateHighlight(selectedSongId) {
    if (currentSongId) { const oldLi = document.getElementById(`song-list-item-${currentSongId}`); if (oldLi) { oldLi.style.backgroundColor = "transparent"; oldLi.classList.remove('highlighted'); } }
    const newLi = document.getElementById(`song-list-item-${selectedSongId}`); if (newLi) { newLi.style.backgroundColor = "var(--bg-hover)"; newLi.classList.add('highlighted'); }
    currentSongId = selectedSongId;
}

function togglePlay() {
    if (!audioEl.src) return;
    if (isPlaying) { audioEl.pause(); playPauseIcon.className = 'fa-solid fa-play'; } else { audioEl.play(); playPauseIcon.className = 'fa-solid fa-pause'; }
    isPlaying = !isPlaying;
}

function rewind10() { if (!audioEl.src) return; audioEl.currentTime = Math.max(0, audioEl.currentTime - 10); }
function forward10() { if (!audioEl.src) return; audioEl.currentTime = Math.min(audioEl.duration, audioEl.currentTime + 10); }

audioEl.addEventListener('loadedmetadata', () => timeTotalEl.textContent = formatTime(audioEl.duration));

let isDraggingSeek = false;
audioEl.addEventListener('timeupdate', () => {
    const current = audioEl.currentTime; const duration = audioEl.duration;
    if (duration) { 
        if (!isDraggingSeek && seekSlider) {
            seekSlider.value = (current / duration) * 100;
            seekSlider.style.background = `linear-gradient(to right, var(--essential-positive) ${seekSlider.value}%, #4d4d4d ${seekSlider.value}%)`;
        }
        timeCurrentEl.textContent = formatTime(current); 
    }
});
audioEl.addEventListener('ended', () => { 
    if (repeatMode === 2) {
        audioEl.currentTime = 0;
        audioEl.play();
        return;
    }
    window.playNext();
    
    if (!isPlaying && audioEl.paused) {
        if (seekSlider) {
            seekSlider.value = 0;
            seekSlider.style.background = '#4d4d4d';
        }
    }
});

if (seekSlider) {
    seekSlider.addEventListener('input', (e) => {
        isDraggingSeek = true;
        const val = e.target.value;
        seekSlider.style.background = `linear-gradient(to right, var(--essential-positive) ${val}%, #4d4d4d ${val}%)`;
        if (audioEl.duration) {
            timeCurrentEl.textContent = formatTime((val / 100) * audioEl.duration);
        }
    });

    seekSlider.addEventListener('change', (e) => {
        isDraggingSeek = false;
        if (audioEl.duration) {
            audioEl.currentTime = (e.target.value / 100) * audioEl.duration;
        }
    });
}

function updateVolume() {
    const val = parseFloat(volumeSlider.value);
    audioEl.volume = Math.max(0, Math.min(1, val));
    volumeSlider.style.background = `linear-gradient(to right, var(--text-base) ${val * 100}%, #4d4d4d ${val * 100}%)`;
    const volIcon = document.getElementById('volume-icon');
    if (volIcon) {
        if (val === 0) volIcon.className = 'fa-solid fa-volume-xmark control-btn';
        else if (val < 0.5) volIcon.className = 'fa-solid fa-volume-low control-btn';
        else volIcon.className = 'fa-solid fa-volume-high control-btn';
    }
}
volumeSlider.addEventListener('input', updateVolume);
if (audioEl.readyState > 0 || volumeSlider) updateVolume();

let lastVolume = 0.7;
window.toggleMute = function() {
    if (audioEl.volume > 0) {
        lastVolume = audioEl.volume;
        volumeSlider.value = 0;
    } else {
        volumeSlider.value = lastVolume > 0 ? lastVolume : 0.7;
    }
    updateVolume();
}

function triggerAIFake(currentId) {
    const aiGrid = document.getElementById('ai-songs-grid'); if(!aiGrid) return;
    aiGrid.innerHTML = '<div class="text-success fw-bold" style="padding:10px;"><i class="fa-solid fa-bolt"></i> Phân tích AI tức thời dựa trên Thể loại và Hồ sơ Nghệ sĩ tương đồng...</div>';
    setTimeout(() => {
        aiGrid.innerHTML = ''; const cur = findSongById(currentId); const visibleSongs = getVisibleSongs();
        let matchArtist = visibleSongs.filter(s => s.id !== currentId && s.artistId !== null && s.artistId === cur?.artistId);
        let matchGenre = visibleSongs.filter(s => s.id !== currentId && s.genre.includes(cur?.genre.split(',')[0]) && s.artistId !== cur?.artistId);
        let recommendations = [...matchArtist, ...matchGenre];
        const others = visibleSongs.filter(s => s.id !== currentId && !recommendations.includes(s));
        recommendations = recommendations.concat(others).slice(0, 8);
        
        recommendations.forEach(song => {
            const item = document.createElement('div'); item.className = 'ai-suggest-item';
            item.style = "display: flex; align-items: center; justify-content: space-between; padding: 10px 12px; border-radius: 6px; cursor: pointer; transition: background-color 0.2s;";
            item.onmouseenter = () => item.style.backgroundColor = "var(--bg-hover)"; item.onmouseleave = () => item.style.backgroundColor = "transparent";
            item.onclick = (e) => playSelectedSong(song.id, e);
            item.innerHTML = `
                <div style="display: flex; align-items: center; gap: 12px; overflow: hidden;">
                    <button style="background: transparent; border: none; color: var(--text-base); cursor: pointer;"><i class="fa-solid fa-play" style="font-size: 14px;"></i></button>
                    <div style="display: flex; flex-direction: column; overflow: hidden;">
                        <span style="font-weight: 600; font-size: 14px; color: var(--text-base); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${song.title}</span>
                        <span class="ai-match-text" style="font-size: 12px; color: var(--essential-positive);"><i class="fa-solid fa-wand-magic-sparkles"></i> Phù hợp ${Math.floor(Math.random() * 10 + 90)}%</span>
                        <span class="ai-hover-info" style="font-size: 11px; color: var(--text-subdued); display: none;">3:45 • ${song.genre}</span>
                    </div>
                </div>
                <div>
                    <button title="Thêm Danh Sách Chờ" onclick="addToQueue(${song.id}, event)" style="background: transparent; border: none; color: var(--text-base); font-size: 14px; cursor: pointer; margin-right: 12px;"><i class="fa-solid fa-square-plus"></i></button>
                    <button title="Thêm Playist" onclick="openAddToPlaylistModal(${song.id}, event)" style="background: transparent; border: none; color: var(--text-subdued); font-size: 14px; cursor: pointer;"><i class="fa-solid fa-plus"></i></button>
                </div>
            `;
            aiGrid.appendChild(item);
        });
    }, 200);
}

let tempFile = null;
function showToast(message) {
    const container = document.getElementById('toast-container'); const toast = document.createElement('div'); toast.className = 'toast';
    toast.innerHTML = `<i class="fa-solid fa-circle-check" style="color: var(--essential-positive); margin-right: 8px;"></i> ${message}`;
    container.appendChild(toast); setTimeout(() => toast.remove(), 3500);
}

const uploadInput = document.getElementById('upload-input'); const uploadModal = document.getElementById('upload-meta-modal');
uploadInput.addEventListener('change', (e) => {
    const file = e.target.files[0]; if (!file) return; tempFile = file;
    document.getElementById('upload-filename').textContent = file.name;
    document.getElementById('meta-title').value = file.name.replace(/\.[^/.]+$/, ""); document.getElementById('meta-artist').value = ""; document.getElementById('meta-genre').value = "";
    uploadModal.classList.add('active'); document.getElementById('meta-title').focus(); uploadInput.value = "";
});

document.getElementById('btn-cancel-meta').addEventListener('click', () => { uploadModal.classList.remove('active'); tempFile = null; });

document.getElementById('btn-submit-meta').addEventListener('click', async () => {
    const finalTitle = document.getElementById('meta-title').value.trim() || (tempFile ? tempFile.name.replace(/\.[^/.]+$/, "") : "My Audio");
    uploadModal.classList.remove('active'); showToast(`Đang tải lên: ${finalTitle}...`);
    await new Promise(resolve => setTimeout(resolve, 1500)); showToast("Precompute hoàn tất. Hệ thống sẵn sàng phân tích AI!");
    
    const newSong = { id: Date.now(), title: finalTitle, artist: document.getElementById('meta-artist').value.trim() || 'Custom Uploads', genre: document.getElementById('meta-genre').value.trim() || 'Unknown Genre', img: "https://picsum.photos/seed/newupload/200/200", url: URL.createObjectURL(tempFile), artistId: null };
    songs.unshift(newSong); 
    goBackToHome(); const t = document.getElementById('search-input')?.value.trim() || ""; renderArtists(t); renderSongs(t); loadAndPlaySong(newSong); tempFile = null;
});

function renderPlaylistsSidebar() {
    const list = document.getElementById('sidebar-playlist-render'); if (!list) return; list.innerHTML = ''; 
    
    const source = getPlaylistSource();
    if (source.length === 0) { 
        const li = document.createElement('li'); li.style = 'color:var(--text-subdued); padding: 12px;'; 
        li.textContent = 'Bạn chưa có playlist (Click dấu + trên thanh để tạo).'; 
        list.appendChild(li); 
        return; 
    }
    source.forEach(pl => {
        const li = document.createElement('li'); li.className = 'artist-item'; li.onclick = () => viewPlaylist(pl.id);
        li.innerHTML = `<img src="https://picsum.photos/seed/playlist${pl.id}/200/200" alt="Playlist" class="artist-avatar" style="border-radius: 4px;"><div class="artist-info"><span class="artist-name">${pl.name}</span><span class="artist-type" id="pl-count-${pl.id}">Playlist • ${pl.songs.length} bài</span></div>`;
        list.appendChild(li);
    });
}

const createPlaylistBtn = document.querySelector('.library-actions button[title="Create playlist"]');
const playlistModal = document.getElementById('playlist-modal');
if(createPlaylistBtn) createPlaylistBtn.addEventListener('click', () => { playlistModal.classList.add('active'); document.getElementById('playlist-name-input').focus(); });
document.getElementById('btn-cancel-playlist').addEventListener('click', () => { playlistModal.classList.remove('active'); document.getElementById('playlist-name-input').value = ''; });
document.getElementById('btn-create-playlist').addEventListener('click', () => {
    const name = document.getElementById('playlist-name-input').value.trim();
    if (name) {
        const newId = Date.now(); 
        playlists.unshift({ id: newId, name: name, songs: [] });
        saveDefaultPlaylists(); 
        renderPlaylistsSidebar(); 
        showToast(`Đã tạo: ${name}`);
        playlistModal.classList.remove('active'); 
        document.getElementById('playlist-name-input').value = ''; 
        viewPlaylist(newId);
    }
});

let pendingAddSongId = null; const addToPlaylistModal = document.getElementById('add-to-playlist-modal');
window.openAddToPlaylistModal = function(songId, event) {
    if(event) event.stopPropagation(); pendingAddSongId = songId; const listEl = document.getElementById('modal-playlist-list'); listEl.innerHTML = ''; const source = getPlaylistSource();
    if (source.length === 0) { listEl.innerHTML = '<li style="color:var(--text-subdued); padding: 10px;">Bạn chưa có playlist nào. Hãy tạo một cái ở thanh trái!</li>'; } 
    else { source.forEach(pl => { const li = document.createElement('li'); li.className = 'modal-playlist-item'; li.innerHTML = `<img src="https://picsum.photos/seed/playlist${pl.id}/200/200"><span>${pl.name}</span><span style="margin-left:auto; font-size: 13px; color: var(--text-subdued);">${pl.songs.length} bài</span>`; li.onclick = () => addSongToPlaylist(pendingAddSongId, pl.id); listEl.appendChild(li); }); }
    addToPlaylistModal.classList.add('active');
};
window.closeAddToPlaylistModal = function() { addToPlaylistModal.classList.remove('active'); pendingAddSongId = null; };
function addSongToPlaylist(songId, playlistId) {
    const pl = getPlaylistSource().find(p => p.id === playlistId);
    if (pl) {
        if (!pl.songs.includes(songId)) { 
            pl.songs.push(songId); 
            saveDefaultPlaylists();
            renderPlaylistsSidebar(); 
            if(document.getElementById('playlist-view').style.display === 'block') viewPlaylist(playlistId); 
            showToast(`Đã thêm vào ${pl.name}`); 
        } 
        else showToast(`Bài hát đã tồn tại`);
    }
    closeAddToPlaylistModal();
}

window.openSongDetail = function(songId, event) {
    if(event) event.stopPropagation(); const song = findSongById(songId);
    if(song) { 
        document.getElementById('detail-img').src = song.img; 
        document.getElementById('detail-title').textContent = song.title; 
        document.getElementById('detail-artist').textContent = song.artist; 
        document.getElementById('detail-genre').textContent = song.genre; 
        document.getElementById('btn-edit-song-img').onclick = () => triggerImageUpload('song', song.id);
        document.getElementById('song-detail-modal').classList.add('active'); 
    }
}

const dashboardView = document.getElementById('dashboard-view'); const playlistView = document.getElementById('playlist-view'); const artistView = document.getElementById('artist-view'); const plViewTitle = document.getElementById('playlist-view-title'); const plViewList = document.getElementById('playlist-view-list');
function goBackToHome() { playlistView.style.display = 'none'; artistView.style.display = 'none'; dashboardView.style.display = 'block'; }

function viewPlaylist(playlistId) {
    const pl = getPlaylistSource().find(p => p.id === playlistId); if(!pl) return;
    dashboardView.style.display = 'none'; artistView.style.display = 'none'; playlistView.style.display = 'block';
    
    document.getElementById('current-playlist-id').value = pl.id; 
    document.getElementById('playlist-view-title').textContent = pl.name;
    document.getElementById('btn-edit-playlist-title').style.display = 'block';
    const deleteBtn = document.getElementById('btn-delete-playlist');
    if (deleteBtn) deleteBtn.style.display = 'block';
    
    plViewList.innerHTML = '';
    if(pl.songs.length === 0) { plViewList.innerHTML = '<li style="color:var(--text-subdued); padding:20px 0;">Playlist rỗng.</li>'; return; }
    pl.songs.forEach((songId) => {
        const songObj = findSongById(songId); if(!songObj) return;
        const li = document.createElement('li'); li.style = "display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--bg-hover); transition: background-color 0.2s;";
        li.onmouseenter = () => li.style.backgroundColor = "var(--bg-highlight)"; li.onmouseleave = () => li.style.backgroundColor = "transparent";
        li.innerHTML = `<div style="width: 40px; text-align: center;"><button onclick="playSelectedSong(${songObj.id}, event)" style="background: transparent; border: none; color: var(--text-base); font-size: 14px; cursor: pointer;"><i class="fa-solid fa-play"></i></button></div><div style="flex: 1; display: flex; align-items: center; gap: 12px;"><img src="${songObj.img}" alt="img" style="width: 40px; height: 40px; border-radius: 4px; object-fit: cover;"><div style="display:flex; flex-direction: column;"><span style="font-weight: 600; color: var(--text-base); cursor: pointer;" onclick="playSelectedSong(${songObj.id})">${songObj.title}</span><span style="font-size: 13px; color: var(--text-subdued);">${songObj.artist}</span></div></div><div style="width: 150px; color: var(--text-subdued); font-size: 13px;">${songObj.genre}</div><div style="width: 80px; text-align: center;">...</div><div style="width: 120px; text-align: center; display: flex; justify-content: center; gap: 16px;"><button onclick="openSongDetail(${songObj.id}, event)" style="background: transparent; color: var(--text-subdued); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-circle-info"></i></button><button title="Thêm Danh Sách Chờ" onclick="addToQueue(${songObj.id}, event)" style="background: transparent; color: var(--text-base); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-square-plus"></i></button><button onclick="removeSongFromPlaylist(${pl.id}, ${songObj.id})" style="background: transparent; color: #e74c3c; border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-trash-can"></i></button></div>`;
        plViewList.appendChild(li);
    });
}

window.removeUpload = function(songId) {
    if (confirm("Bạn có chắc muốn xóa vĩnh viễn bài hát này khỏi hệ thống?")) {
        const idx = songs.findIndex(s => s.id === songId);
        if (idx > -1) songs.splice(idx, 1);
        showToast("Đã xóa bài hát tải lên");
        renderSongs(document.getElementById('search-input')?.value.trim() || "");
        renderHabitAndTrendingSongs();
        renderPlaylistsSidebar();
    }
}

function removeSongFromPlaylist(playlistId, songId) {
    const pl = playlists.find(p => p.id === playlistId);
    if(pl) { 
        pl.songs = pl.songs.filter(id => id !== songId); 
        saveDefaultPlaylists();
        showToast("Đã gỡ bài hát"); 
        renderPlaylistsSidebar(); 
        viewPlaylist(playlistId); 
    }
}

window.deleteCurrentPlaylist = function() {
    const plId = parseInt(document.getElementById('current-playlist-id').value);
    if (!plId) return;
    if (confirm("Bạn có chắc chắn muốn xóa playlist này?")) {
        const idx = playlists.findIndex(p => p.id === plId);
        if (idx > -1) {
            playlists.splice(idx, 1);
            saveDefaultPlaylists();
        }
        renderPlaylistsSidebar();
        goBackToHome();
        showToast("Đã xóa playlist");
    }
};

window.editPlaylistTitle = function() {
    const idStr = document.getElementById('current-playlist-id').value;
    if (idStr === "my_music") return; 
    const id = parseInt(idStr); 
    const pl = getPlaylistSource().find(p => p.id === id); if(!pl) return;
    
    const titleEl = document.getElementById('playlist-view-title'); const btnEl = document.getElementById('btn-edit-playlist-title');
    const input = document.createElement('input'); input.type = 'text'; input.value = pl.name; input.className = 'inline-edit-input'; input.id = 'playlist-view-title';
    
    const saveNewTitle = () => { 
        const newName = input.value.trim(); 
        if(newName && newName !== pl.name) { 
            pl.name = newName; 
            showToast("Đã đổi tên!"); 
            saveDefaultPlaylists();
            renderPlaylistsSidebar(); 
        }  
        const newH1 = document.createElement('h1');
        newH1.id = 'playlist-view-title';
        newH1.style = "font-size: 32px; font-weight: 700; margin: 0;";
        newH1.textContent = pl.name;
        if(input.parentNode) input.parentNode.replaceChild(newH1, input);
        btnEl.style.display = 'block'; 
    };
    input.addEventListener('blur', saveNewTitle); input.addEventListener('keydown', (e) => { if (e.key === 'Enter') input.blur(); });
    
    if(titleEl.parentNode) titleEl.parentNode.replaceChild(input, titleEl); 
    btnEl.style.display = 'none'; input.focus();
};

function viewArtist(artistId) {
    const ar = artists.find(a => a.id === artistId); if(!ar) return;
    dashboardView.style.display = 'none'; playlistView.style.display = 'none'; artistView.style.display = 'block';
    
    const arImgEl = document.getElementById('artist-view-img');
    if (arImgEl) arImgEl.src = ar.img;
    document.getElementById('btn-edit-artist-img').onclick = () => triggerImageUpload('artist', artistId);
    
    document.getElementById('artist-view-title').textContent = ar.name;
    const arList = document.getElementById('artist-view-list'); arList.innerHTML = '';
    const arSongs = songs.filter(s => s.artistId === artistId);
    if(arSongs.length === 0) { arList.innerHTML = '<li style="color:var(--text-subdued); padding:20px 0;">Chưa có bài hát.</li>'; return; }
    arSongs.forEach((songObj) => {
        const li = document.createElement('li'); li.style = "display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--bg-hover); transition: background-color 0.2s;";
        li.onmouseenter = () => li.style.backgroundColor = "var(--bg-highlight)"; li.onmouseleave = () => li.style.backgroundColor = "transparent";
        li.innerHTML = `<div style="width: 40px; text-align: center;"><button onclick="playSelectedSong(${songObj.id}, event)" style="background: transparent; border: none; color: var(--text-base); font-size: 14px; cursor: pointer;"><i class="fa-solid fa-play"></i></button></div><div style="flex: 1; display: flex; align-items: center; gap: 12px;"><img src="${songObj.img}" alt="img" style="width: 40px; height: 40px; border-radius: 4px; object-fit: cover;"><div style="display:flex; flex-direction: column;"><span style="font-weight: 600; color: var(--text-base); cursor: pointer;" onclick="playSelectedSong(${songObj.id})">${songObj.title}</span><span style="font-size: 13px; color: var(--text-subdued);">${songObj.artist}</span></div></div><div style="width: 150px; color: var(--text-subdued); font-size: 13px;">${songObj.genre}</div><div style="width: 120px; text-align: center; display: flex; justify-content: center; gap: 16px;"><button onclick="openSongDetail(${songObj.id}, event)" style="background: transparent; color: var(--text-subdued); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-circle-info"></i></button><button onclick="openAddToPlaylistModal(${songObj.id}, event)" style="background: transparent; color: var(--text-base); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-plus"></i></button><button title="Thêm Danh Sách Chờ" onclick="addToQueue(${songObj.id}, event)" style="background: transparent; color: var(--text-base); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-square-plus"></i></button></div>`;
        arList.appendChild(li);
    });
}

window.addToQueue = function(id, event) {
    if (event) event.stopPropagation();
    if (!playQueue.includes(id)) {
        playQueue.push(id);
        showToast("Đã thêm vào danh sách chờ");
        if (document.getElementById('queue-modal').classList.contains('active')) renderQueue();
    } else {
        showToast("Bài hát đã có trong danh sách chờ");
    }
}

window.openQueueModal = function() {
    document.getElementById('queue-modal').classList.add('active');
    renderQueue();
};

window.removeFromQueue = function(index) {
    playQueue.splice(index, 1);
    renderQueue();
}

let draggedItemIndex = null;
function renderQueue() {
    const currentContainer = document.getElementById('queue-current-song');
    const queueList = document.getElementById('queue-list');
    
    if (currentSongId) {
        const curSong = findSongById(currentSongId);
        currentContainer.innerHTML = `
            <img src="${curSong.img}" style="width: 48px; height: 48px; border-radius: 4px; object-fit: cover;">
            <div style="display: flex; flex-direction: column;">
                <span style="font-weight: 700; color: var(--text-base);">${curSong.title}</span>
                <span style="font-size: 13px; color: var(--text-subdued);">${curSong.artist}</span>
            </div>
            <i class="fa-solid fa-volume-high" style="margin-left: auto; color: var(--essential-positive);"></i>
        `;
    } else {
        currentContainer.innerHTML = '<span style="color: var(--text-subdued);">Không có bài hát nào đang phát</span>';
    }

    queueList.innerHTML = '';
    if (playQueue.length === 0) {
        queueList.innerHTML = '<li style="color:var(--text-subdued); padding: 10px;">Danh sách chờ trống.</li>';
        return;
    }

    playQueue.forEach((songId, index) => {
        const song = findSongById(songId);
        if (!song) return;
        const li = document.createElement('li');
        li.className = 'queue-drag-item';
        li.draggable = true;
        li.dataset.index = index;
        
        li.innerHTML = `
            <i class="fa-solid fa-grip-vertical"></i>
            <img src="${song.img}" style="width: 40px; height: 40px; border-radius: 4px; object-fit: cover;">
            <div style="display: flex; flex-direction: column; flex: 1;">
                <span style="font-size: 14px; font-weight: 600; color: var(--text-base);">${song.title}</span>
                <span style="font-size: 12px; color: var(--text-subdued);">${song.artist}</span>
            </div>
            <button onmousedown="event.stopPropagation()" onclick="removeFromQueue(${index})" style="background: transparent; border: none; color: var(--text-subdued); cursor: pointer; padding: 8px;"><i class="fa-solid fa-xmark" style="font-size: 16px;"></i></button>
        `;

        li.addEventListener('dragstart', (e) => {
            draggedItemIndex = index;
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/plain', index);
            setTimeout(() => li.style.opacity = '0.5', 0);
        });

        li.addEventListener('dragend', () => {
            li.style.opacity = '1';
            document.querySelectorAll('.queue-drag-item').forEach(item => item.classList.remove('drag-over'));
            draggedItemIndex = null;
        });

        li.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            li.classList.add('drag-over');
        });

        li.addEventListener('dragleave', () => {
            li.classList.remove('drag-over');
        });

        li.addEventListener('drop', (e) => {
            e.preventDefault();
            li.classList.remove('drag-over');
            const draggedIdx = parseInt(e.dataTransfer.getData('text/plain'));
            const targetIdx = index;
            if (draggedIdx === targetIdx || isNaN(draggedIdx)) return;
            
            const [movedItem] = playQueue.splice(draggedIdx, 1);
            playQueue.splice(targetIdx, 0, movedItem);
            renderQueue();
        });

        queueList.appendChild(li);
    });
}