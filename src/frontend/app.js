// --- 0. CẤU HÌNH API ---
const API_URL = "http://localhost:8000";

// --- 1. DỮ LIỆU CỐ ĐỊNH (Artists) ---
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

// --- 2. QUẢN LÝ DỮ LIỆU BÀI HÁT (API) ---
let songs = [];

async function fetchSongs() {
    try {
        const response = await fetch(`${API_URL}/songs/`);
        const serverSongs = await response.json();
        
        // Chuẩn hóa dữ liệu từ Server sang định dạng Frontend expect
        const mappedServerSongs = serverSongs.map(s => {
            // Tìm kiếm hoặc khởi tạo Nghệ sĩ mới nếu chưa có trong mảng artists
            let existingArtist = artists.find(a => a.name.toLowerCase() === s.artist.toLowerCase());
            if (!existingArtist) {
                existingArtist = { 
                    id: Date.now() + Math.floor(Math.random() * 1000), 
                    name: s.artist, 
                    img: `https://ui-avatars.com/api/?name=${encodeURIComponent(s.artist)}&background=random&color=fff&size=300` 
                };
                artists.push(existingArtist);
            }
            
            return {
                id: s.id,
                title: s.title,
                artist: s.artist,
                genre: s.genre || null,            // The loai CHINH - cho AI
                sub_genres: s.sub_genres || null,  // Tags phu - hien thi UI
                duration: s.duration || 0,
                img: `https://picsum.photos/seed/${s.id}/200/200`,
                url: `${API_URL}/songs/${s.id}/stream`,
                artistId: existingArtist.id,
                isServer: true
            };
        });
        
        songs = [...mappedServerSongs];
        renderSongs();
        renderHabitAndTrendingSongs();
        if (typeof renderArtistOptions === 'function') renderArtistOptions();
        if (typeof renderArtists === 'function') renderArtists();
    } catch (error) {
        console.error("Không thể kết nối Backend:", error);
    }
}

let playlists = [];

async function fetchPlaylists() {
    try {
        const response = await fetch(`${API_URL}/playlists/`);
        playlists = await response.json();
        renderPlaylistsSidebar();
    } catch (error) {
        console.error("Lỗi lấy danh sách playlist:", error);
    }
}

function saveDefaultPlaylists() {
    // Không còn dùng localStorage cho playlist, Backend sẽ quản lý
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

/** Chuyển đổi giây sang định dạng m:ss */
function formatDuration(seconds) {
    if (!seconds || seconds <= 0) return '--:--';
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}

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
            <div style="width: 150px; font-size: 13px;">
                ${songObj.genre ? `<span style="display:inline-block; background: rgba(29,185,84,0.15); color: var(--essential-positive); font-weight: 700; font-size: 11px; padding: 2px 8px; border-radius: 500px; margin-bottom: 2px;">${songObj.genre}</span>` : ''}
                ${songObj.sub_genres ? `<br><span style="color: var(--text-subdued); font-size: 11px;">${songObj.sub_genres}</span>` : (!songObj.genre ? `<span style="color: var(--text-subdued);">Chưa phân loại</span>` : '')}
            </div>
            <div style="width: 80px; text-align: center; color: var(--text-subdued);">${formatDuration(songObj.duration)}</div>
            <div style="width: 140px; text-align: center; display: flex; justify-content: center; gap: 12px;">
                <button title="Tạo AI Radio" onclick="generateSmartPlaylist(${songObj.id}, event)" style="background: transparent; color: var(--essential-positive); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-wand-magic-sparkles"></i></button>
                <button title="Chi tiết" onclick="openSongDetail(${songObj.id}, event)" style="background: transparent; color: var(--text-subdued); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-circle-info"></i></button>
                <button title="Thêm Playlist" onclick="openAddToPlaylistModal(${songObj.id}, event)" style="background: transparent; color: var(--text-subdued); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-plus"></i></button>
                <button title="Thêm Danh Sách Chờ" onclick="addToQueue(${songObj.id}, event)" style="background: transparent; color: var(--text-base); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-square-plus"></i></button>
                <button title="Xóa Vĩnh Viễn" onclick="removeUpload(${songObj.id}, event)" style="background: transparent; color: #e74c3c; border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-trash-can"></i></button>
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
        const plView = document.getElementById('playlist-view');
        const artistView = document.getElementById('artist-view');
        
        if (plView && plView.style.display === 'block') {
            const plId = parseInt(document.getElementById('current-playlist-id').value);
            const pl = playlists.find(p => p.id === plId);
            if (pl && pl.songs) {
                currentPlaylistContext = pl.songs.map(s => s.id || s);
            }
        } else if (artistView && artistView.style.display === 'block') {
            const artistTitle = document.getElementById('artist-view-title').textContent;
            currentPlaylistContext = getVisibleSongs().filter(s => s.artist === artistTitle).map(s => s.id);
        } else {
            currentPlaylistContext = getVisibleSongs().map(s => s.id);
        }
        
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
            isPlaying = false; playPauseIcon.className = 'fa-solid fa-play';
            showToast("Lỗi khi phát bài hát này.");
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

async function triggerAIFake(currentId) {
    const aiGrid = document.getElementById('ai-songs-grid'); if(!aiGrid) return;
    const currentSong = findSongById(currentId);

    // Nếu là nhạc không thuộc server (Mock fallback), dùng logic gợi ý Meta
    if (!currentSong || !currentSong.isServer) {
        aiGrid.innerHTML = '<div class="text-success fw-bold" style="padding:10px;"><i class="fa-solid fa-wand-magic-sparkles"></i> Gợi ý thông minh dựa trên Thể loại & Nghệ sĩ...</div>';
        setTimeout(() => {
            aiGrid.innerHTML = ''; 
            const visibleSongs = getVisibleSongs();
            let recommendations = visibleSongs.filter(s => s.id !== currentId && (s.artistId === currentSong?.artistId || (currentSong?.genre && s.genre.includes(currentSong.genre.split(',')[0])))).slice(0, 5);
            
            if (recommendations.length === 0) recommendations = visibleSongs.filter(s => s.id !== currentId).sort(() => 0.5 - Math.random()).slice(0, 5);
            
            renderRecommendationList(recommendations);
        }, 300);
        return;
    }

    aiGrid.innerHTML = '<div class="text-success fw-bold" style="padding:10px;"><i class="fa-solid fa-bolt"></i> AI đang phân tích sóng âm tương đồng...</div>';
    
    try {
        const response = await fetch(`${API_URL}/recommend/${currentId}`);
        if (!response.ok) {
            if (response.status === 503) throw new Error("503");
            throw new Error(`API Error: ${response.status}`);
        }
        const data = await response.json();
        const recommendIds = data.recommended_ids;

        aiGrid.innerHTML = '';
        if (!recommendIds || recommendIds.length === 0) {
            aiGrid.innerHTML = '<div style="font-style: italic; color: var(--text-subdued); font-size: 13px;">Chưa tìm thấy bài hát tương đồng nào trên hệ thống.</div>';
            return;
        }

        const recommendations = recommendIds.map(rid => findSongById(rid)).filter(s => s);
        renderRecommendationList(recommendations);
        
    } catch (error) {
        if (error.message === "503") {
            aiGrid.innerHTML = '<div style="color: var(--text-subdued); font-size: 13px;"><i class="fa-solid fa-hourglass-half"></i> AI đang phân tích bài hát này... Bạn thử lại sau ít phút nhé.</div>';
        } else {
            console.error("Lỗi Engine AI:", error);
            aiGrid.innerHTML = '<div style="color: #e74c3c; font-size: 13px;"><i class="fa-solid fa-triangle-exclamation"></i> Lỗi kết nối AI.</div>';
        }
    }
}

function renderRecommendationList(recommendations) {
    const aiGrid = document.getElementById('ai-songs-grid');
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
                    <span class="ai-match-text" style="font-size: 11px; color: var(--essential-positive);"><i class="fa-solid fa-wand-magic-sparkles"></i> Phù hợp ${Math.floor(Math.random() * 5 + 93)}%</span>
                </div>
            </div>
        `;
        aiGrid.appendChild(item);
    });
}

let tempFile = null;
function showToast(message) {
    const container = document.getElementById('toast-container'); const toast = document.createElement('div'); toast.className = 'toast';
    toast.innerHTML = `<i class="fa-solid fa-circle-check" style="color: var(--essential-positive); margin-right: 8px;"></i> ${message}`;
    container.appendChild(toast); setTimeout(() => toast.remove(), 3500);
}

const uploadInput = document.getElementById('upload-input'); 
const aiModal = document.getElementById('ai-analyze-modal');
const uploadModal = document.getElementById('upload-meta-modal');

let currentAnalysis = null;

uploadInput.addEventListener('change', async (e) => {
    const file = e.target.files[0]; if (!file) return; tempFile = file;
    document.getElementById('upload-filename').textContent = file.name;
    document.getElementById('meta-title').value = file.name.replace(/\.[^/.]+$/, ""); 
    document.getElementById('meta-artist').value = ""; 
    document.getElementById('meta-genre').value = "";
    uploadInput.value = "";
    
    // Mở popup tiến trình AI
    aiModal.classList.add('active');
    document.getElementById('ai-analyze-loading').style.display = 'block';
    document.getElementById('ai-analyze-result').style.display = 'none';

    // Gọi API phân tích
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_URL}/songs/analyze`, { method: 'POST', body: formData });
        if (!response.ok) throw new Error("Lỗi Analyze");
        currentAnalysis = await response.json();
        
        // Cập nhật UI với kết quả
        document.getElementById('ai-analyze-loading').style.display = 'none';
        document.getElementById('ai-predicted-genre').textContent = currentAnalysis.predicted_genre !== 'Unknown' ? currentAnalysis.predicted_genre : 'Không xác định';
        document.getElementById('ai-confidence').textContent = currentAnalysis.predicted_genre !== 'Unknown' ? `(${currentAnalysis.confidence.toFixed(0)}%)` : '';
        document.getElementById('ai-analyze-result').style.display = 'block';
        
    } catch (err) {
        // Fallback nếu lỗi trích xuất
        aiModal.classList.remove('active');
        uploadModal.classList.add('active');
        showToast("Lỗi phân tích AI. Vui lòng nhập tay.");
    }
});

// Nút Đúng rồi (Accept AI)
document.getElementById('btn-ai-accept').addEventListener('click', () => {
    aiModal.classList.remove('active');
    document.getElementById('meta-genre').value = currentAnalysis.predicted_genre !== 'Unknown' ? currentAnalysis.predicted_genre : '';
    document.getElementById('upload-temp-path').value = currentAnalysis.temp_path;
    uploadModal.classList.add('active');
});

// Nút Chỉnh lại (Reject AI)
document.getElementById('btn-ai-reject').addEventListener('click', () => {
    aiModal.classList.remove('active');
    document.getElementById('upload-temp-path').value = currentAnalysis.temp_path;
    uploadModal.classList.add('active');
    document.getElementById('meta-genre').focus();
});

document.getElementById('btn-cancel-meta').addEventListener('click', () => { 
    uploadModal.classList.remove('active'); 
    tempFile = null; 
    currentAnalysis = null;
});

function renderArtistOptions() {
    const list = document.getElementById('artist-options');
    if (list) list.innerHTML = artists.map(a => `<option value="${a.name}">`).join('');
}
renderArtistOptions(); // Gọi lúc khởi tạo

document.getElementById('btn-submit-meta').addEventListener('click', async () => {
    const title = document.getElementById('meta-title').value.trim();
    const artist = document.getElementById('meta-artist').value.trim() || "Unknown";
    const genre = document.getElementById('meta-genre').value.trim();
    const tempPath = document.getElementById('upload-temp-path').value;

    if (!title) { showToast("Vui lòng nhập tiêu đề bài hát!"); return; }

    uploadModal.classList.remove('active');
    showToast(`Đang lưu thông tin bài hát: ${title}...`);

    try {
        const response = await fetch(`${API_URL}/songs/confirm`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                artist: artist,
                genre: genre,
                temp_path: tempPath
            })
        });

        if (!response.ok) throw new Error("Upload thất bại");

        const result = await response.json();
        showToast("Tải lên thành công! File đã được lưu.");
        
        await fetchSongs();
        const newSong = songs.find(s => s.id === result.id);
        if (newSong) loadAndPlaySong(newSong);
        
        tempFile = null;
        currentAnalysis = null;
    } catch (error) {
        console.error("Lỗi Upload:", error);
        showToast("Lỗi hệ thống khi xác nhận bài hát.");
    }
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
document.getElementById('btn-create-playlist').addEventListener('click', async () => {
    const name = document.getElementById('playlist-name-input').value.trim();
    if (name) {
        try {
            const response = await fetch(`${API_URL}/playlists/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: name })
            });
            const newPl = await response.json();
            
            playlists.unshift(newPl);
            renderPlaylistsSidebar(); 
            showToast(`Đã tạo: ${name}`);
            playlistModal.classList.remove('active'); 
            document.getElementById('playlist-name-input').value = ''; 
            viewPlaylist(newPl.id);
        } catch (error) {
            console.error("Lỗi tạo playlist:", error);
            showToast("Không thể tạo playlist trên server.");
        }
    }
});

let pendingAddSongId = null; const addToPlaylistModal = document.getElementById('add-to-playlist-modal');
window.openAddToPlaylistModal = function(songId, event) {
    if(event) event.stopPropagation(); pendingAddSongId = songId; const listEl = document.getElementById('modal-playlist-list'); listEl.innerHTML = ''; const source = getPlaylistSource();
    if (source.length === 0) { listEl.innerHTML = '<li style="color:var(--text-subdued); padding: 10px;">Bạn chưa có playlist nào. Hãy tạo một cái ở thanh trái!</li>'; } 
    else { source.forEach(pl => { const li = document.createElement('li'); li.className = 'modal-playlist-item'; li.style = "display: flex; align-items: center; gap: 12px; padding: 10px; border-radius: 8px; cursor: pointer; transition: background 0.2s; margin-bottom: 4px;"; li.onmouseenter = () => li.style.background = "var(--bg-hover)"; li.onmouseleave = () => li.style.background = "transparent"; li.innerHTML = `<img src="https://picsum.photos/seed/playlist${pl.id}/200/200" style="width: 48px; height: 48px; border-radius: 8px; object-fit: cover; flex-shrink: 0;"><span style="font-weight: 600; font-size: 15px; color: var(--text-base);">${pl.name}</span><span style="margin-left:auto; font-size: 13px; color: var(--text-subdued);">${pl.songs.length} bài</span>`; li.onclick = () => addSongToPlaylist(pendingAddSongId, pl.id); listEl.appendChild(li); }); }
    addToPlaylistModal.classList.add('active');
};
window.closeAddToPlaylistModal = function() { addToPlaylistModal.classList.remove('active'); pendingAddSongId = null; };
async function addSongToPlaylist(songId, playlistId) {
    const pl = playlists.find(p => p.id === playlistId);
    if (pl) {
        // Kiểm tra xem song có trong pl.songs (array of objects) chưa
        if (!pl.songs.some(s => s.id === songId)) { 
            try {
                const response = await fetch(`${API_URL}/playlists/${playlistId}/songs/${songId}`, {
                    method: 'POST'
                });
                if (!response.ok) throw new Error("Lỗi add song");
                
                // Cập nhật local state để UI mượt mà
                const songObj = findSongById(songId);
                if (songObj) pl.songs.push(songObj);
                
                renderPlaylistsSidebar(); 
                if(document.getElementById('playlist-view').style.display === 'block') viewPlaylist(playlistId); 
                showToast(`Đã thêm vào ${pl.name}`); 
            } catch (error) {
                console.error("Lỗi thêm bài hát:", error);
                showToast("Lỗi server khi thêm nhạc.");
            }
        } 
        else showToast(`Bài hát đã tồn tại`);
    }
    closeAddToPlaylistModal();
}

window.openSongDetail = function(songId, event) {
    if(event) event.stopPropagation(); const song = findSongById(songId);
    if(song) { 
        document.getElementById('detail-img').src = song.img || `https://picsum.photos/seed/${song.id}/200/200`; 
        
        const titleEl = document.getElementById('detail-title');
        const artistEl = document.getElementById('detail-artist');
        const inputTitle = document.getElementById('edit-detail-title');
        const inputArtist = document.getElementById('edit-detail-artist');
        const toggleBtn = document.getElementById('btn-toggle-edit-meta');
        const saveBtn = document.getElementById('btn-save-song-meta');
        
        titleEl.textContent = song.title; 
        artistEl.textContent = song.artist; 
        document.getElementById('detail-genre').textContent = song.genre; 
        document.getElementById('btn-edit-song-img').onclick = () => triggerImageUpload('song', song.id);
        
        // Reset Edit Modal states
        titleEl.style.display = 'block';
        artistEl.style.display = 'block';
        inputTitle.style.display = 'none';
        inputArtist.style.display = 'none';
        saveBtn.style.display = 'none';
        inputTitle.value = song.title;
        inputArtist.value = song.artist;
        toggleBtn.style.color = 'var(--text-subdued)';

        // Toggle edit logic
        toggleBtn.onclick = () => {
            if (titleEl.style.display === 'block') {
                titleEl.style.display = 'none';
                artistEl.style.display = 'none';
                inputTitle.style.display = 'block';
                inputArtist.style.display = 'block';
                saveBtn.style.display = 'block';
                toggleBtn.style.color = 'var(--text-base)';
            } else {
                titleEl.style.display = 'block';
                artistEl.style.display = 'block';
                inputTitle.style.display = 'none';
                inputArtist.style.display = 'none';
                saveBtn.style.display = 'none';
                toggleBtn.style.color = 'var(--text-subdued)';
            }
        };

        const generateBtn = document.getElementById('btn-create-smart-playlist');
        if (generateBtn) {
            generateBtn.onclick = () => {
                document.getElementById('song-detail-modal').classList.remove('active');
                generateSmartPlaylist(song.id);
            };
        }

        // Save logic
        saveBtn.onclick = async () => {
            const newTitle = inputTitle.value.trim();
            const newArtist = inputArtist.value.trim();
            if(!newTitle) { showToast("Tên bài hát không được để trống!"); return; }
            
            try {
                const response = await fetch(`${API_URL}/songs/${song.id}`, {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title: newTitle, artist: newArtist || "Unknown" })
                });
                
                if (!response.ok) throw new Error("Update failed");
                const updatedSong = await response.json();
                
                // Cập nhật lại array local
                song.title = updatedSong.title;
                song.artist = updatedSong.artist;

                // Xử lý auto-complete Artist (Cập nhật mục Nghệ Sĩ ở màn hình chính)
                let existingArtist = artists.find(a => a.name.toLowerCase() === updatedSong.artist.toLowerCase());
                if (!existingArtist) {
                    existingArtist = { id: Date.now(), name: updatedSong.artist, img: `https://ui-avatars.com/api/?name=${encodeURIComponent(updatedSong.artist)}&background=random&color=fff&size=300` };
                    artists.unshift(existingArtist);
                    if (typeof renderArtistOptions === 'function') renderArtistOptions();
                    if (typeof renderArtists === 'function') renderArtists();
                }

                // Tắt edit mode
                titleEl.textContent = song.title;
                artistEl.textContent = song.artist;
                toggleBtn.onclick(); 
                
                showToast("Đã lưu thay đổi thông tin bài hát!");
                
                // Re-render UI
                const searchVal = document.getElementById('search-input')?.value.trim() || "";
                renderSongs(searchVal);
                renderHabitAndTrendingSongs();
                renderPlaylistsSidebar();
                
                // Update player in-sync
                if(currentSongId === song.id) {
                    document.getElementById('player-title').textContent = song.title;
                    document.getElementById('player-artist').textContent = song.artist;
                }
                
                // Refresh playlist view if open
                const currentPlId = document.getElementById('current-playlist-id').value;
                if(currentPlId && currentPlId !== 'my_music' && document.getElementById('playlist-view').style.display === 'block') {
                    viewPlaylist(parseInt(currentPlId));
                }
                
            } catch (error) {
                console.error("Lỗi cập nhật bài hát:", error);
                showToast("Lỗi máy chủ khi cập nhật thông tin!");
            }
        };

        document.getElementById('song-detail-modal').classList.add('active'); 
    }
}

const dashboardView = document.getElementById('dashboard-view'); const playlistView = document.getElementById('playlist-view'); const artistView = document.getElementById('artist-view'); const plViewTitle = document.getElementById('playlist-view-title'); const plViewList = document.getElementById('playlist-view-list');
function goBackToHome() { playlistView.style.display = 'none'; artistView.style.display = 'none'; dashboardView.style.display = 'block'; }

function viewPlaylist(playlistId) {
    const pl = playlists.find(p => p.id === playlistId); if(!pl) return;
    dashboardView.style.display = 'none'; artistView.style.display = 'none'; playlistView.style.display = 'block';
    
    document.getElementById('current-playlist-id').value = pl.id; 
    document.getElementById('playlist-view-title').textContent = pl.name;
    document.getElementById('btn-edit-playlist-title').style.display = 'block';
    const deleteBtn = document.getElementById('btn-delete-playlist');
    if (deleteBtn) deleteBtn.style.display = 'block'; // Sẽ cập nhật logic DELETE sau nếu cần
    
    plViewList.innerHTML = '';
    if(!pl.songs || pl.songs.length === 0) { plViewList.innerHTML = '<li style="color:var(--text-subdued); padding:20px 0;">Playlist rỗng.</li>'; return; }
    
    // pl.songs hiện là mảng các object hoặc IDs. Với API Response mới, nó là mảng Objects.
    pl.songs.forEach((songObj) => {
        const li = document.createElement('li'); li.style = "display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--bg-hover); transition: background-color 0.2s;";
        li.onmouseenter = () => li.style.backgroundColor = "var(--bg-highlight)"; li.onmouseleave = () => li.style.backgroundColor = "transparent";
        li.innerHTML = `<div style="width: 40px; text-align: center;"><button onclick="playSelectedSong(${songObj.id}, event)" style="background: transparent; border: none; color: var(--text-base); font-size: 14px; cursor: pointer;"><i class="fa-solid fa-play"></i></button></div><div style="flex: 1; display: flex; align-items: center; gap: 12px;"><img src="${songObj.img || `https://picsum.photos/seed/${songObj.id}/200/200`}" alt="img" style="width: 40px; height: 40px; border-radius: 4px; object-fit: cover;"><div style="display:flex; flex-direction: column;"><span style="font-weight: 600; color: var(--text-base); cursor: pointer;" onclick="playSelectedSong(${songObj.id})">${songObj.title}</span><span style="font-size: 13px; color: var(--text-subdued);">${songObj.artist}</span></div></div><div style="width: 150px; color: var(--text-subdued); font-size: 13px;">${songObj.genre || "Pop"}</div><div style="width: 80px; text-align: center;">...</div><div style="width: 120px; text-align: center; display: flex; justify-content: center; gap: 16px;"><button onclick="openSongDetail(${songObj.id}, event)" style="background: transparent; color: var(--text-subdued); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-circle-info"></i></button><button title="Thêm Danh Sách Chờ" onclick="addToQueue(${songObj.id}, event)" style="background: transparent; color: var(--text-base); border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-square-plus"></i></button><button onclick="removeSongFromPlaylist(${pl.id}, ${songObj.id})" style="background: transparent; color: #e74c3c; border: none; font-size: 16px; cursor: pointer;"><i class="fa-solid fa-trash-can"></i></button></div>`;
        plViewList.appendChild(li);
    });
}

window.removeUpload = async function(songId, event) {
    if(event) event.stopPropagation();
    if (confirm("🚨 BẠN CHẮC CHẮN MUỐN XÓA VĨNH VIỄN BÀI HÁT NÀY KHỎI DỰ ÁN?\n\nFile .mp3, Dữ liệu sóng âm và mọi liên kết Playlist sẽ bay màu. Hành động này không thể hoàn tác!")) {
        try {
            const response = await fetch(`${API_URL}/songs/${songId}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error("Delete failed");
            
            // Xóa state array local
            const idx = songs.findIndex(s => s.id === songId);
            if (idx > -1) songs.splice(idx, 1);
            
            showToast("Đã xóa bài hát vĩnh viễn khỏi toàn hệ thống!");
            
            // Cập nhật lại giao diện
            renderSongs(document.getElementById('search-input')?.value.trim() || "");
            renderHabitAndTrendingSongs();
            renderPlaylistsSidebar();
        } catch (error) {
            console.error("Lỗi xóa bài hát:", error);
            showToast("Không thể xóa bài hát! Có lỗi xảy ra từ máy chủ.");
        }
    }
}

async function removeSongFromPlaylist(playlistId, songId) {
    const pl = playlists.find(p => p.id === playlistId);
    if(pl) { 
        try {
            const response = await fetch(`${API_URL}/playlists/${playlistId}/songs/${songId}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error("Delete failed");
            
            pl.songs = pl.songs.filter(s => {
                const sId = typeof s === 'object' ? s.id : s;
                return sId !== songId;
            });
            showToast("Đã gỡ bài hát"); 
            renderPlaylistsSidebar(); 
            viewPlaylist(playlistId); 
        } catch (error) {
            console.error("Lỗi xoá bài hát:", error);
            showToast("Lỗi khi xoá bài hát khỏi server.");
        }
    }
}

window.deleteCurrentPlaylist = async function() {
    const plId = parseInt(document.getElementById('current-playlist-id').value);
    if (!plId) return;
    if (confirm("Bạn có chắc chắn muốn xóa playlist này?")) {
        try {
            const response = await fetch(`${API_URL}/playlists/${plId}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error("Delete failed");
            
            const idx = playlists.findIndex(p => p.id === plId);
            if (idx > -1) playlists.splice(idx, 1);
            
            renderPlaylistsSidebar();
            goBackToHome();
            showToast("Đã xóa playlist");
        } catch (error) {
            console.error("Lỗi xoá playlist:", error);
            showToast("Lỗi khi xoá playlist trên server.");
        }
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

window.generateSmartPlaylist = async function(songId, event) {
    if (event) event.stopPropagation();
    
    const song = findSongById(songId);
    if (!song) return;

    showToast(`AI đang phân tích & tổng hợp Radio cho: ${song.title}...`);

    try {
        const response = await fetch(`${API_URL}/playlists/smart`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                song_id: songId,
                limit: 15,
                name: `Radio: ${song.title}`
            })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        const newPlaylist = await response.json();
        
        playlists.unshift(newPlaylist);
        renderPlaylistsSidebar();
        
        showToast(`Đã tạo thành công AI Radio cho bài hát này!`);
        viewPlaylist(newPlaylist.id);

    } catch (error) {
        console.error("Lỗi khi tạo Smart Playlist:", error);
        showToast("Không thể tạo mạng lưới bài hát. Vui lòng thử lại sau!");
    }
}

fetchSongs();
fetchPlaylists();
