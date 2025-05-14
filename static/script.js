let resultData = null;

document.querySelectorAll('.result-tab').forEach(tab => {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.result-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

        this.classList.add('active');

        const tabId = this.getAttribute('data-tab');
        document.getElementById(tabId + '-tab').classList.add('active');
    });
});

document.getElementById('search-btn').addEventListener('click', function() {
    const username = document.getElementById('username').value.trim();
    if (!username) {
        alert('Vui lòng nhập tên người dùng');
        return;
    }

    const websites = document.getElementById('websites').value.trim();
    const metadata = document.getElementById('metadata').checked;
    const extract = document.getElementById('extract').checked;

    document.getElementById('loading').style.display = 'block';
    document.getElementById('result-container').style.display = 'none';

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            websites: websites,
            metadata: metadata,
            extract: extract
        }),
    })
    .then(response => response.json())
    .then(data => {
        resultData = data;
        document.getElementById('loading').style.display = 'none';
        document.getElementById('result-container').style.display = 'block';
        document.getElementById('result-username').textContent = username;

        // dữ liệu JSON
        document.getElementById('raw-json').textContent = JSON.stringify(data, null, 2);

        // dữ liệu card
        renderProfileCards(data);
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        alert('Đã xảy ra lỗi: ' + error);
    });
});

document.getElementById('download-btn').addEventListener('click', function() {
    if (!resultData) return;

    const dataStr = JSON.stringify(resultData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);

    const exportFileDefaultName = 'social-analyzer-result.json';

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
});

function renderProfileCards(data) {
    console.log("dữ liệu:",data);
    const container = document.getElementById('profiles-container');
    container.innerHTML = '';

    if (data.detected && Array.isArray(data.detected) && data.detected.length > 0) {
        data.detected.forEach((profile, index) => {
            const card = document.createElement('div');
            card.className = 'profile-card';
            card.dataset.index = index;
            card.style.paddingLeft = '15px';

            const header = document.createElement('div');
            header.className = 'profile-header';

            const icon = document.createElement('div');
            icon.className = 'profile-icon';
            icon.textContent = profile.title ? profile.title.charAt(0).toUpperCase() : '?';

            const siteName = document.createElement('div');
            siteName.className = 'profile-site';
            siteName.textContent = profile.title || 'Unknown';

            const status = document.createElement('div');
            status.className = 'profile-status';
            status.textContent = profile.status || 'Unknown';

            header.appendChild(icon);
            header.appendChild(siteName);
            header.appendChild(status);

            card.appendChild(header);

            const infoContainer = document.createElement('div');
            infoContainer.className = 'profile-info';

            const infoFields = [
                { label: 'country', value: profile.country },
                { label: 'extracted', value: profile.extracted },
                { label: 'found', value: profile.found },
                { label: 'language', value: profile.language },
                { label: 'Link', value: profile.link }
            ];

            infoFields.forEach(field => {
                if (field.value) {
                    const paragraph = document.createElement('p');
                    paragraph.style.marginLeft = '15px';
                    paragraph.textContent = `${field.label}: ${field.value}`;
                    infoContainer.appendChild(paragraph);
                }
            });

            card.appendChild(infoContainer);

            card.addEventListener('click', () => showProfileDetails(profile));
            container.appendChild(card);
        });
    } else {
        container.innerHTML = '<div class="no-results">Không có kết quả nào được tìm thấy.</div>';
    }
}

function showProfileDetails(profile) {
    const modal = document.getElementById('profile-modal');
    const contentContainer = document.getElementById('profile-modal-content');
    modal.style.display = 'block';
    modal.style.width = '600px';
    modal.style.height = '500px';
    contentContainer.innerHTML = '';

    const title = document.createElement('h3');
    title.textContent = profile.title || 'Chi tiết người dùng';
    contentContainer.appendChild(title);

    const infoFields = [
        { label: 'country', value: profile.country },
        { label: 'language', value: profile.language },
        { label: 'found', value: profile.rank },
        { label: 'rate', value: profile.rate },
        { label: 'content', value: profile.text },
        { label: 'type', value: profile.type }
    ];

    infoFields.forEach(field => {
        if (field.value) {
            const paragraph = document.createElement('p');
            paragraph.textContent = `${field.label}: ${field.value}`;
            contentContainer.appendChild(paragraph);
        }
    });

    if (profile.metadata && profile.metadata.length > 0) {
        const metadataSection = document.createElement('div');
        metadataSection.innerHTML = '<h4>Metadata</h4>';
        const metadataList = document.createElement('ul');
        profile.metadata.forEach(meta => {
            const metaItem = document.createElement('li');
            metaItem.textContent = `${meta.name}: ${meta.content}`;
            metadataList.appendChild(metaItem);
        });
        metadataSection.appendChild(metadataList);
        contentContainer.appendChild(metadataSection);
    }

    const imageMeta = profile.metadata?.find(meta => meta.property === 'og:image');
    if (imageMeta) {
        const image = document.createElement('img');
        image.src = imageMeta.content;
        image.alt = 'Profile Image';
        image.style.maxWidth = '100%';
        contentContainer.appendChild(image);
    }

    if (profile.link) {
        const link = document.createElement('a');
        link.href = profile.link;
        link.textContent = 'Truy cập hồ sơ';
        link.target = '_blank';
        contentContainer.appendChild(link);
    }

    document.getElementById('close-modal').onclick = () => {
        modal.style.display = 'none';
    };
}





