const API = "http://127.0.0.1:5000";

const bookmarksDiv = document.getElementById("bookmarks");
const statsDiv = document.getElementById("stats");
const message = document.getElementById("message");
const pageInfo = document.getElementById("pageInfo");

let currentPage = 1;
const perPage = 5;

function showMessage(text, color = "#d9534f") {
  message.style.color = color;
  message.textContent = text;
}

function toggleEdit(id) {
  const section = document.getElementById(`editSection${id}`);
  section.style.display = section.style.display === "none" ? "block" : "none";
}

async function refresh() {
  const refreshToken = localStorage.getItem('refreshToken');
  console.log("called refresh1");
  console.log(refreshToken === null )
  if ( refreshToken=== null) {
    showMessage("No refresh token found. Please log in.");
    window.location.href = "index.html";
  }

  try {
    const res = await fetch(`${API}/refresh`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${refreshToken}`
      }
    });

    const result = await res.json();

    localStorage.setItem('accessToken', result.access_token);
    showMessage("Session refreshed", "#28a745");
  } catch (error) {
    console.error("Error refreshing token:", error);
  }
}

function getAccessToken() {
  return localStorage.getItem('accessToken');
}

async function loadBookmarks(page = 1) {
  currentPage = page;
  try {
    const res = await fetch(`${API}/?page=${page}&per_page=${perPage}`, {
      method: "GET",
      headers: { Authorization: `Bearer ${getAccessToken()}` }
    });
    const data = await res.json();
    if (!res.ok) {
      showMessage(data.message || "Failed to load bookmarks.");
      return;
    }

    bookmarksDiv.innerHTML = "";
    statsDiv.innerHTML = "";
    pageInfo.textContent = `Page ${data.meta.page} of ${data.meta.pages}`;

    data.data.forEach(bookmark => {
      const div = document.createElement("div");
      div.className = "bookmark";
      div.innerHTML = `
        <strong>${bookmark.body}</strong><br/>
        <a href="${API}/${bookmark.short_url}" target="_blank">${bookmark.url}</a>
        <div class="meta">
          ID: ${bookmark.id} |
          Created: ${new Date(bookmark.created_at).toLocaleString()} |
          Visits: ${bookmark.visits}
        </div>
        <button onclick="toggleEdit(${bookmark.id})">✏️ Update</button>
        <div id="editSection${bookmark.id}" style="display:none;">
          <textarea id="editBody${bookmark.id}">${bookmark.body}</textarea>
          <input type="url" id="editUrl${bookmark.id}" value="${bookmark.url}" />
          <button onclick="submitUpdate(${bookmark.id})">💾 Save</button>
        </div>
        <button onclick="deleteBookmark(${bookmark.id})">🗑️ Delete</button>
      `;
      bookmarksDiv.appendChild(div);
    });

    document.getElementById("prevPage").disabled = !data.meta.has_prev;
    document.getElementById("nextPage").disabled = !data.meta.has_next;
  } catch {
    showMessage("Failed to load bookmarks.");
  }
}

async function submitUpdate(id) {
  const body = document.getElementById(`editBody${id}`).value;
  const url = document.getElementById(`editUrl${id}`).value;

  try {
    const res = await fetch(`${API}/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify({ body, url })
    });
    const data = await res.json();
    if (!res.ok) return showMessage(data.message || "Update failed.");
    showMessage("Updated!", "#28a745");
    loadBookmarks(currentPage);
  } catch {
    showMessage("Error updating.");
  }
}

async function deleteBookmark(id) {
  try {
    const res = await fetch(`${API}/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${getAccessToken()}` }
    });
    if (!res.ok) return showMessage("Delete failed");
    showMessage("Deleted!", "#dc3545");
    loadBookmarks(currentPage);
  } catch {
    showMessage("Error deleting.");
  }
}

async function logout() {
  try {
    const res = await fetch(`${API}/logout`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getAccessToken()}`
      }
    });

    const data = await res.json();
    console.log("Logout response:", data);

    if (!res.ok) {
      showMessage("Logout failed: " + (data.message || res.statusText));
      return;
    }

    showMessage("Logged out successfully!", "#007bff");
  } catch (err) {
    console.error("Logout error:", err);
    showMessage("Logout error.");
  } finally {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    window.location.href = "index.html"; 
  }
}

document.getElementById("bookmarkForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const body = document.getElementById("body").value;
  const url = document.getElementById("url").value;

  try {
    const res = await fetch(`${API}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify({ body, url })
    });
    const data = await res.json();
    if (!res.ok) return showMessage(data.message);
    showMessage("Bookmark added!", "#28a745");
    document.getElementById("bookmarkForm").reset();
    loadBookmarks(currentPage);
  } catch {
    showMessage("Error saving bookmark.");
  }
});

document.getElementById("loadAll").addEventListener("click", () => loadBookmarks());
document.getElementById("prevPage").addEventListener("click", () => loadBookmarks(currentPage - 1));
document.getElementById("nextPage").addEventListener("click", () => loadBookmarks(currentPage + 1));

document.getElementById("loadStats").addEventListener("click", async () => {
  try {
    const res = await fetch(`${API}/get_stats`, {
      method: "GET",
      headers: { Authorization: `Bearer ${getAccessToken()}` }
    });
    const data = await res.json();
    statsDiv.innerHTML = "<h3>Stats</h3>";
    data.data.forEach(bm => {
      console.log(bm)
      const block = document.createElement("div");
      block.className = "bookmark";
      block.innerHTML = `<strong>${bm.body}</strong><br/>Visits: ${bm.visits}<br/>ID: ${bm.id}<br/>Created at: ${bm.created_at}<br/>Short URL: ${bm.short_url}`;
      statsDiv.appendChild(block);
    });
  } catch {
    showMessage("Failed to load stats.");
  }
});

document.getElementById("getById").addEventListener("click", async () => {
  const id = document.getElementById("searchId").value;
  if (!id) return showMessage("Enter a valid ID");

  try {
    const res = await fetch(`${API}/${id}`, {
      method: "GET",
      headers: { Authorization: `Bearer ${getAccessToken()}` }
    });
    const data = await res.json();
    if (!res.ok) return showMessage("Bookmark not found");

    bookmarksDiv.innerHTML = `
      <div class="bookmark">
        <strong>${data.body}</strong><br/>
        <a href="${API}/r/${data.short_url}" target="_blank">${data.url}</a>
        <div class="meta">
          ID: ${data.id} |
          Created: ${new Date(data.created_at).toLocaleString()} |
          Visits: ${data.visits}
        </div>
        <button onclick="toggleEdit(${data.id})">✏️ Update</button>
        <div id="editSection${data.id}" style="display:none;">
          <textarea id="editBody${data.id}">${data.body}</textarea>
          <input type="url" id="editUrl${data.id}" value="${data.url}" />
          <button onclick="submitUpdate(${data.id})">💾 Save</button>
        </div>
        <button onclick="deleteBookmark(${data.id})">🗑️ Delete</button>
      </div>
    `;
    statsDiv.innerHTML = "";
    pageInfo.textContent = "";
  } catch {
    showMessage("Error fetching bookmark.");
  }
});

// Attach logout button handler
document.getElementById("logout").addEventListener("click", logout);

// 🔄 Preload bookmarks immediately on page load
window.onload = async () => {
  await refresh();

};
