import pytest
from fastapi import status


class TestPosts:
    """Test post endpoints."""
    
    def test_create_post_success(self, client, auth_headers):
        """Test successful post creation."""
        post_data = {
            "title": "Test Post",
            "content": "This is a test post content.",
            "published": True
        }
        
        response = client.post("/api/v1/posts/", json=post_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == post_data["title"]
        assert data["content"] == post_data["content"]
        assert data["published"] == post_data["published"]
        assert "id" in data
        assert "author_id" in data
    
    def test_create_post_unauthorized(self, client):
        """Test post creation without authentication."""
        post_data = {
            "title": "Test Post",
            "content": "This is a test post content.",
            "published": True
        }
        
        response = client.post("/api/v1/posts/", json=post_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_posts(self, client, auth_headers):
        """Test getting all posts."""
        # Create a post first
        post_data = {
            "title": "Test Post",
            "content": "This is a test post content.",
            "published": True
        }
        client.post("/api/v1/posts/", json=post_data, headers=auth_headers)
        
        response = client.get("/api/v1/posts/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_posts_published_only(self, client, auth_headers):
        """Test getting only published posts."""
        # Create published post
        published_post = {
            "title": "Published Post",
            "content": "This is published.",
            "published": True
        }
        client.post("/api/v1/posts/", json=published_post, headers=auth_headers)
        
        # Create draft post
        draft_post = {
            "title": "Draft Post",
            "content": "This is a draft.",
            "published": False
        }
        client.post("/api/v1/posts/", json=draft_post, headers=auth_headers)
        
        response = client.get("/api/v1/posts/?published_only=true")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(post["published"] for post in data)
    
    def test_get_post_by_id(self, client, auth_headers):
        """Test getting a specific post by ID."""
        # Create a post first
        post_data = {
            "title": "Test Post",
            "content": "This is a test post content.",
            "published": True
        }
        create_response = client.post("/api/v1/posts/", json=post_data, headers=auth_headers)
        post_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/posts/{post_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == post_id
        assert data["title"] == post_data["title"]
    
    def test_get_post_not_found(self, client):
        """Test getting a non-existent post."""
        response = client.get("/api/v1/posts/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Post not found" in response.json()["detail"]
    
    def test_update_post_success(self, client, auth_headers):
        """Test successful post update."""
        # Create a post first
        post_data = {
            "title": "Original Title",
            "content": "Original content.",
            "published": False
        }
        create_response = client.post("/api/v1/posts/", json=post_data, headers=auth_headers)
        post_id = create_response.json()["id"]
        
        # Update the post
        update_data = {
            "title": "Updated Title",
            "content": "Updated content.",
            "published": True
        }
        
        response = client.put(f"/api/v1/posts/{post_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["content"] == update_data["content"]
        assert data["published"] == update_data["published"]
    
    def test_update_post_unauthorized(self, client, auth_headers, test_user2):
        """Test updating another user's post."""
        # Create a post with test_user
        post_data = {
            "title": "Test Post",
            "content": "Test content.",
            "published": True
        }
        create_response = client.post("/api/v1/posts/", json=post_data, headers=auth_headers)
        post_id = create_response.json()["id"]
        
        # Try to update with different user (test_user2)
        # First login as test_user2
        login_response = client.post("/api/v1/auth/login", data={
            "username": "testuser2",
            "password": "testpassword2"
        })
        user2_headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        update_data = {"title": "Unauthorized Update"}
        response = client.put(f"/api/v1/posts/{post_id}", json=update_data, headers=user2_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Not enough permissions" in response.json()["detail"]
    
    def test_delete_post_success(self, client, auth_headers):
        """Test successful post deletion."""
        # Create a post first
        post_data = {
            "title": "Post to Delete",
            "content": "This post will be deleted.",
            "published": True
        }
        create_response = client.post("/api/v1/posts/", json=post_data, headers=auth_headers)
        post_id = create_response.json()["id"]
        
        response = client.delete(f"/api/v1/posts/{post_id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify post is deleted
        get_response = client.get(f"/api/v1/posts/{post_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_post_unauthorized(self, client, auth_headers, test_user2):
        """Test deleting another user's post."""
        # Create a post with test_user
        post_data = {
            "title": "Test Post",
            "content": "Test content.",
            "published": True
        }
        create_response = client.post("/api/v1/posts/", json=post_data, headers=auth_headers)
        post_id = create_response.json()["id"]
        
        # Try to delete with different user (test_user2)
        login_response = client.post("/api/v1/auth/login", data={
            "username": "testuser2",
            "password": "testpassword2"
        })
        user2_headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        response = client.delete(f"/api/v1/posts/{post_id}", headers=user2_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Not enough permissions" in response.json()["detail"]
    
    def test_get_my_posts(self, client, auth_headers):
        """Test getting current user's posts."""
        # Create posts
        post_data1 = {
            "title": "My Post 1",
            "content": "First post.",
            "published": True
        }
        post_data2 = {
            "title": "My Post 2",
            "content": "Second post.",
            "published": False
        }
        client.post("/api/v1/posts/", json=post_data1, headers=auth_headers)
        client.post("/api/v1/posts/", json=post_data2, headers=auth_headers)
        
        response = client.get("/api/v1/posts/my/posts", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
