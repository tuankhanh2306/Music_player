/**
 * File: lyric_player.js
 * Chức năng: Hệ thống Lời bài hát Fullscreen (Spotify Style)
 * Nhiệm vụ: Kinetic scrolling, Blurred background, Sync cực mượt.
 */

class LyricPlayer {
    constructor() {
        this.audioEl = document.getElementById('real-audio-player');
        this.lyricOverlay = null;
        this.lyricWrapper = null;
        this.bgLayer = null;
        this.parsedLyrics = [];
        this.currentLineIndex = -1;
        this.currentLineIndex = -1;
        this.isOpen = false;
        this.rawLrc = ""; // Lưu chuỗi LRC gốc (AI sinh ra hoặc người dùng đã sửa)
        this.currentSongId = null;
        this.rawLrc = "";
        this.songId = null;

        this.initUI();
        this.initEvents();
    }

    initUI() {
        // Tạo Fullscreen Overlay (Spotify Style)
        const overlay = document.createElement('div');
        overlay.id = 'lyric-overlay';
        overlay.className = 'lyric-overlay'; // CSS tự ẩn mặc định bằng opacity/visibility
        overlay.innerHTML = `
            <div class="lyric-bg-layer" id="lyric-bg-layer"></div>
            <div class="lyric-overlay-content">
                <div class="lyric-overlay-header">
                    <div class="lyric-header-info">
                         <img src="" id="lyric-mini-img" class="lyric-mini-img">
                         <div class="lyric-header-text">
                            <div id="lyric-header-title" class="lyric-header-title">Đang phát...</div>
                            <div id="lyric-header-artist" class="lyric-header-artist">Nghệ sĩ</div>
                         </div>
                    </div>
                    <div style="display: flex; gap: 12px; align-items: center;">
                        <button class="btn-lyric-edit" id="btn-open-lyric-edit" title="Chỉnh sửa lời bài hát">
                            <i class="fa-solid fa-pen"></i>
                        </button>
                        <button class="lyric-full-close" id="btn-close-full-lyrics">
                            <i class="fa-solid fa-chevron-down"></i>
                        </button>
                    </div>
                </div>
                <div class="lyric-viewport">
                    <div class="lyric-kinetic-container" id="lyric-kinetic-container">
                        <!-- Lời nhạc sẽ render ở đây -->
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
        this.lyricOverlay = overlay;
        this.lyricWrapper = document.getElementById('lyric-kinetic-container');
        this.bgLayer = document.getElementById('lyric-bg-layer');

        // Sự kiện đóng
        document.getElementById('btn-close-full-lyrics').onclick = () => this.toggle(false);

        // Sự kiện Sửa lời
        document.getElementById('btn-open-lyric-edit').onclick = () => this.openEditModal();
        document.getElementById('btn-close-lyric-edit').onclick = () => this.closeEditModal();
        document.getElementById('btn-cancel-lyric-edit').onclick = () => this.closeEditModal();
        document.getElementById('btn-save-lyric-edit').onclick = () => this.saveLyrics();

        // Đếm dòng textarea
        document.getElementById('lyric-edit-textarea').oninput = (e) => {
            const count = e.target.value.split('\n').filter(l => l.trim()).length;
            document.getElementById('lyric-edit-lines-count').textContent = `${count} dòng lời`;
        };

        // Time Shift
        const btnMinus = document.getElementById('btn-shift-minus');
        const btnPlus = document.getElementById('btn-shift-plus');
        if (btnMinus) btnMinus.onclick = () => this.shiftTime(-1);
        if (btnPlus) btnPlus.onclick = () => this.shiftTime(1);

        // Đóng bằng phím ESC
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                if (document.getElementById('lyric-edit-modal').classList.contains('active')) {
                    this.closeEditModal();
                } else {
                    this.toggle(false);
                }
            }
        });
    }

    initEvents() {
        if (this.audioEl) {
            this.audioEl.addEventListener('timeupdate', () => this.syncLyrics());
        }
    }

    parseLRC(lrcText) {
        if (!lrcText) return [];
        const lines = lrcText.split('\n');
        const lyrics = [];
        const lrcRegex = /\[(\d{2}):(\d{2})\.(\d{2})\](.*)/;

        lines.forEach(line => {
            const match = line.match(lrcRegex);
            if (match) {
                const m = parseInt(match[1]);
                const s = parseInt(match[2]);
                const ms = parseInt(match[3]);
                const time = m * 60 + s + ms / 100;
                const text = match[4].trim();
                if (text) lyrics.push({ time, text });
            }
        });
        return lyrics.sort((a, b) => a.time - b.time);
    }

    async fetchLyrics(songId) {
        if (!songId) return;

        this.parsedLyrics = [];
        this.currentLineIndex = -1;
        this.lyricWrapper.style.transform = `translateY(0px)`;
        this.lyricWrapper.innerHTML = '<div class="lyric-placeholder-full"><i class="fa-solid fa-microphone-slash"></i> Đang chuẩn bị lời bài hát AI...</div>';

        try {
            const response = await fetch(`${API_URL}/songs/${songId}/lyrics`);
            const data = await response.json();

            if (data.has_lyrics && data.lrc_content) {
                this.rawLrc = data.lrc_content;
                this.songId = songId;
                this.parsedLyrics = this.parseLRC(data.lrc_content);
                this.renderLyrics();

                // Cập nhật thông tin trên header
                this.updateHeaderInfo();
            } else {
                this.lyricWrapper.innerHTML = '<div class="lyric-placeholder-full">AI đang xử lý lời cho bài hát này... <br> Quay lại sau 30-60 giây nhé!</div>';
            }
        } catch (error) {
            console.error("Lyrics error:", error);
            this.lyricWrapper.innerHTML = '<div class="lyric-placeholder-full">Không thể kết nối máy chủ lời bài hát.</div>';
        }
    }

    updateHeaderInfo() {
        // Lấy thông tin từ Player Bar đang hiển thị
        const title = document.getElementById('player-title').textContent;
        const artist = document.getElementById('player-artist').textContent;
        const img = document.getElementById('player-img').src;

        document.getElementById('lyric-header-title').textContent = title;
        document.getElementById('lyric-header-artist').textContent = artist;
        document.getElementById('lyric-mini-img').src = img;
        this.bgLayer.style.backgroundImage = `url('${img}')`;
    }

    renderLyrics() {
        this.lyricWrapper.innerHTML = '';
        this.parsedLyrics.forEach((line, index) => {
            const div = document.createElement('div');
            div.className = 'lyric-line-full';
            div.id = `full-lyric-line-${index}`;
            div.textContent = line.text;

            div.onclick = (e) => {
                e.stopPropagation();
                this.audioEl.currentTime = line.time;
            };

            this.lyricWrapper.appendChild(div);
        });
    }

    syncLyrics() {
        if (!this.isOpen || this.parsedLyrics.length === 0) return;

        const currentTime = this.audioEl.currentTime;
        let index = -1;

        for (let i = 0; i < this.parsedLyrics.length; i++) {
            if (currentTime >= this.parsedLyrics[i].time) {
                index = i;
            } else {
                break;
            }
        }

        if (index !== -1 && index !== this.currentLineIndex) {
            const lines = document.querySelectorAll('.lyric-line-full');
            lines.forEach((l, i) => {
                if (i === index) l.classList.add('active');
                else if (i < index) l.classList.add('passed');
                else {
                    l.classList.remove('active');
                    l.classList.remove('passed');
                }
            });

            this.currentLineIndex = index;

            const currentEl = document.getElementById(`full-lyric-line-${index}`);
            if (currentEl) {
                const viewportHeight = document.querySelector('.lyric-viewport').offsetHeight;
                const lineOffsetTop = currentEl.offsetTop;

                // Căn dòng active vào giữa viewport
                const offset = (viewportHeight * 0.45) - lineOffsetTop;
                this.lyricWrapper.style.transform = `translateY(${offset}px)`;
            }
        }
    }

    toggle(forceState) {
        this.isOpen = forceState !== undefined ? forceState : !this.isOpen;
        if (this.isOpen) {
            this.lyricOverlay.classList.add('active');       // Hiện ra bằng class .active
            document.body.style.overflow = 'hidden';
            this.updateHeaderInfo();
            if (window.currentSongId) this.fetchLyrics(window.currentSongId);
        } else {
            this.lyricOverlay.classList.remove('active');    // Ẩn đi bằng cách xóa .active
            document.body.style.overflow = '';
        }
    }

    openEditModal() {
        const modal = document.getElementById('lyric-edit-modal');
        const textarea = document.getElementById('lyric-edit-textarea');
        if (!modal || !textarea) return;

        textarea.value = this.rawLrc || "";
        const count = textarea.value.split('\n').filter(l => l.trim()).length;
        document.getElementById('lyric-edit-lines-count').textContent = `${count} dòng lời`;

        modal.classList.add('active');
    }

    closeEditModal() {
        document.getElementById('lyric-edit-modal').classList.remove('active');
    }

    async saveLyrics() {
        if (!this.songId) return;
        const newLrc = document.getElementById('lyric-edit-textarea').value.trim();
        if (!newLrc) {
            showToast("Vui lòng không để trống lời bài hát!");
            return;
        }

        const btn = document.getElementById('btn-save-lyric-edit');
        const originalText = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Đang lưu...';

        try {
            const response = await fetch(`${API_URL}/songs/${this.songId}/lyrics`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lrc_content: newLrc })
            });

            if (!response.ok) throw new Error("Lỗi cập nhật lyric");

            const data = await response.json();

            // Cập nhật state cục bộ
            this.rawLrc = data.lrc_content;
            this.parsedLyrics = this.parseLRC(data.lrc_content);
            this.renderLyrics();

            showToast("Đã cập nhật lời bài hát thành công!");
            this.closeEditModal();
        } catch (error) {
            console.error("Save lyrics error:", error);
            showToast("Lỗi khi lưu bài hát. Thử lại sau!");
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalText;
        }
    }

    shiftTime(offsetSeconds) {
        const textarea = document.getElementById('lyric-edit-textarea');
        if (!textarea) return;

        let content = textarea.value;
        if (!content.trim()) return;

        const lines = content.split('\n');
        const lrcRegex = /^\[(\d{2}):(\d{2})\.(\d{2,3})\](.*)$/;

        const newLines = lines.map(line => {
            const match = line.match(lrcRegex);
            if (match) {
                const m = parseInt(match[1]);
                const s = parseInt(match[2]);
                const ms = parseInt(match[3]);
                let timeInSeconds = m * 60 + s + (ms / (match[3].length === 3 ? 1000 : 100));
                
                timeInSeconds += offsetSeconds;
                if (timeInSeconds < 0) timeInSeconds = 0;

                const newM = Math.floor(timeInSeconds / 60);
                const newS = Math.floor(timeInSeconds % 60);
                // Extract decimal part, keep 2 digits
                let newMs = Math.round((timeInSeconds % 1) * 100);
                if (newMs === 100) {
                    newS += 1;
                    newMs = 0;
                }

                // Format back
                const strM = newM.toString().padStart(2, '0');
                const strS = newS.toString().padStart(2, '0');
                const strMs = newMs.toString().padStart(2, '0');

                return `[${strM}:${strS}.${strMs}]${match[4]}`;
            }
            return line; // Preserve non-lrc lines
        });

        textarea.value = newLines.join('\n');
        if (typeof showToast === 'function') {
            showToast(`Đã ${offsetSeconds > 0 ? 'tiến' : 'lùi'} toàn bộ thời gian ${Math.abs(offsetSeconds)} giây`);
        }
    }
}

// Global hook
window.lyricPlayer = new LyricPlayer();
window.toggleLyricPanel = () => {
    window.lyricPlayer.toggle();
};
