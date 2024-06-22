from abc import ABC, abstractmethod

# Společné rozhraní pro platební brány
class PaymentGatewayAdapter(ABC):
    @abstractmethod
    def process_payment(self, request):
        pass

# Třídy pro platební požadavky a odpovědi
class PaymentRequest:
    def __init__(self, customer_info, payment_details, order_info):
        self.customer_info = customer_info
        self.payment_details = payment_details
        self.order_info = order_info

class PaymentResponse:
    def __init__(self, status, transaction_id):
        self.status = status
        self.transaction_id = transaction_id

# Stripe Adaptér
class StripePaymentRequest:
    def __init__(self, customer_info, payment_details, order_info):
        self.customer_info = customer_info
        self.payment_details = payment_details
        self.order_info = order_info

class StripePaymentResponse:
    def __init__(self, status, transaction_id):
        self.status = status
        self.transaction_id = transaction_id

class StripeClient:
    @staticmethod
    def process_payment(request):
        # Simulace zpracování platby přes Stripe
        print("Zpracování platby přes Stripe...")
        return StripePaymentResponse("Úspěch", "Stripe12345")

class StripeAdapter(PaymentGatewayAdapter):
    def process_payment(self, request: PaymentRequest) -> PaymentResponse:
        stripe_request = StripePaymentRequest(
            request.customer_info, request.payment_details, request.order_info
        )
        stripe_response = StripeClient.process_payment(stripe_request)
        return PaymentResponse(stripe_response.status, stripe_response.transaction_id)

# PayPal Adaptér
class PayPalPaymentRequest:
    def __init__(self, customer_info, payment_details, order_info):
        self.customer_info = customer_info
        self.payment_details = payment_details
        self.order_info = order_info

class PayPalPaymentResponse:
    def __init__(self, status, transaction_id):
        self.status = status
        self.transaction_id = transaction_id

class PayPalClient:
    @staticmethod
    def process_payment(request):
        # Simulace zpracování platby přes PayPal
        print("Zpracování platby přes PayPal...")
        return PayPalPaymentResponse("Úspěch", "PayPal67890")

class PayPalAdapter(PaymentGatewayAdapter):
    def process_payment(self, request: PaymentRequest) -> PaymentResponse:
        paypal_request = PayPalPaymentRequest(
            request.customer_info, request.payment_details, request.order_info
        )
        paypal_response = PayPalClient.process_payment(paypal_request)
        return PaymentResponse(paypal_response.status, paypal_response.transaction_id)

# Adaptér pro platbu hotovostí
class CashAdapter(PaymentGatewayAdapter):
    def process_payment(self, request: PaymentRequest) -> PaymentResponse:
        # Simulace zpracování platby hotovostí
        print(f"Zpracování platby hotovostí pro zákazníka {request.customer_info}...")
        return PaymentResponse("Úspěch", "CashTransaction")

# Kód e-commerce platformy
class HotelPayment:
    def __init__(self, payment_gateway_adapter: PaymentGatewayAdapter):
        self.payment_gateway_adapter = payment_gateway_adapter

    def process_payment(self, request: PaymentRequest) -> PaymentResponse:
        return self.payment_gateway_adapter.process_payment(request)

# Příklad použití
if __name__ == "__main__":
    payment_request_online_card = PaymentRequest(
        customer_info="Customer A",
        payment_details="Credit Card",
        order_info="Online Reservation #1234"
    )

    payment_request_online_paypal = PaymentRequest(
        customer_info="Customer B",
        payment_details="PayPal",
        order_info="Online Reservation #5678"
    )

    payment_request_desk_cash = PaymentRequest(
        customer_info="Customer C",
        payment_details="Cash",
        order_info="Desk Payment for Parking"
    )

    # Použití Stripe Adapteru pro online platbu kartou
    stripe_adapter = StripeAdapter()
    hotel_platform_online_card = HotelPayment(stripe_adapter)
    stripe_response_online_card = hotel_platform_online_card.process_payment(payment_request_online_card)
    print(f"Stripe Stav platby: {stripe_response_online_card.status}, ID transakce: {stripe_response_online_card.transaction_id}")

    # Použití PayPal Adapteru pro online platbu PayPal
    paypal_adapter = PayPalAdapter()
    hotel_platform_online_paypal = HotelPayment(paypal_adapter)
    paypal_response_online_paypal = hotel_platform_online_paypal.process_payment(payment_request_online_paypal)
    print(f"PayPal Stav platby: {paypal_response_online_paypal.status}, ID transakce: {paypal_response_online_paypal.transaction_id}")

    # Použití Cash Adapteru pro platbu na recepci hotovostí
    cash_adapter = CashAdapter()
    hoyel_platform_desk_cash = HotelPayment(cash_adapter)
    cash_response_desk_cash = hoyel_platform_desk_cash.process_payment(payment_request_desk_cash)
    print(f"Cash Stav platby: {cash_response_desk_cash.status}, ID transakce: {cash_response_desk_cash.transaction_id}")