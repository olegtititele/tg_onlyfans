from yoomoney import Authorize

CLIENT_ID = "8AC292B9A641D8DD3D389D7E812A65CB7D2D7FF6573BC38CF1ED45724AEABDB8"

Authorize(
      client_id=CLIENT_ID,
      redirect_uri="https://google.com",
      scope=["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop",
             ]
      )