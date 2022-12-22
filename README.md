# NFT Listing
This is test test project about NFT-Listing for [Authic](https://authic.io/).

# Environment
Environments store in `docker-compose.env`. described below:
- `DB_NAME`: database name (default `nft`)
- `DB_HOST`: database host (default `db`)
- `DB_PORT`: database port (default `3306`)
- `DB_USER`: database username (default `root`)
- `DB_PASS`: database password (default `secret`)

# Run

First your need build docker images:

    docker-compose build

Run:

    docker-compose up -d

Now make sure about migrations:

    docker-compose exec app python manage.py makemigrations
    docker-compose exec app python manage.py migrate

for tests:

    docker-compose exec app python manage.py test
  

# API

- Register:
  - url: `/api/auth/register/`
  - method: `POST`
  - body:
      ```jsonc
      {
          "username": <string>,
          "email": <emailString>,
          "password": <string>,
          "is_seller": <bool>, // optional (default false)
      }
      ```
  - response:
      ```jsonc
      { ...
          "token": <apiToken>,
       ...
      }
      ```
- Login:
  - url: `/api/auth/login/`
  - method: `POST`
  - body:
      ```jsonc
      {
          "username": <string>,
          "password": <string>,
      }
      ```

- Add Listing:
  - url: `/api/nft/listings/add`
  - method: `POST`
  - header: `Authorization: Token {apiToken}`
  - permission: `Seller`
  - body:
    ```jsonc
    {
        "nft": <string>,
        "fixed_price": <int>,
        "view_count": <int>, // optional (default 0)
    }
    ```
- Get Listings:
  - url: `/api/nft/listings/`
  - method: `GET`
  - header: `Authorization: Token {apiToken}`
  - permission: `Seller - Buyer`
  - query parameters:
    - `ordering`=`fixed_price` | `-fixed_price` | `view_count` | `-view_count`
- Get Offers:
  - url: `/api/nft/offers/`
  - method: `GET`
  - header: `Authorization: Token {apiToken}`
  - permission: `Buyer`
- Add Offer:
  - url: `/api/nft/offers/add`
  - method: `POST`
  - header: `Authorization: Token {apiToken}`
  - permission: `Buyer`
  - body:
    ```jsonc
    {
        "listing_id": <int>,
        "price": <int>,
    }
    ```
- Determine Offer:
  - url: `/api/nft/offers/<int:offer_id>/`
  - method: `POST`
  - header: `Authorization: Token {apiToken}`
  - permission: `Seller`
  - body:
    ```jsonc
    {
        "status": <int> // 1 (reject) or 2 (accept)
    }
    ```