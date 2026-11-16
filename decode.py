import pyotp

def decode_otp_secret_and_generate(encoded_secret_with_spaces: str):
    """
    Decodes a Base32 encoded OTP secret (potentially with spaces)
    and demonstrates how to use it to generate a TOTP.

    Args:
        encoded_secret_with_spaces: The Base32 encoded secret string,
                                    which may contain spaces.
    """
    # 1. Remove spaces from the input string
    clean_secret = encoded_secret_with_spaces.replace(" ", "")
    print(f"Cleaned Base32 Secret: {clean_secret}")

    # 2. Decode the Base32 secret
    # Base32 decoding often requires the input to be uppercase and padded correctly.
    # pyotp handles this automatically when given the base32 key,
    # but for manual decoding, you'd convert to uppercase and handle padding if needed.
    try:
        # pyotp's TOTP expects the base32 encoded key directly.
        # It handles the internal decoding.
        totp = pyotp.TOTP(clean_secret)

        print("\n--- OTP Parameters (Common Defaults) ---")
        print(f"Secret Key (Base32): {clean_secret}")
        print(f"Algorithm: SHA1 (default for TOTP in pyotp)")
        print(f"Digits: 6 (default for TOTP in pyotp)")
        print(f"Period: 30 seconds (default for TOTP in pyotp)")

        # 3. Generate a current OTP
        current_otp = totp.now()
        print(f"\nGenerated Current OTP: {current_otp}")

        # 4. Verify an OTP (example)
        # You would typically get an OTP from the user and verify it.
        # For demonstration, let's try verifying the one we just generated.
        is_valid = totp.verify(current_otp)
        print(f"Verification of generated OTP '{current_otp}': {is_valid}")

        # If you needed the raw byte secret (e.g., for different libraries or custom implementation)
        # You would typically do:
        # raw_secret_bytes = base32.b32decode(clean_secret.upper().encode('utf-8'))
        # print(f"Raw Secret Bytes (example): {raw_secret_bytes}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure the Base32 string is valid.")


# Your provided OTP setup code
otp_code_string = "aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa"

decode_otp_secret_and_generate(otp_code_string)

# Example of a different valid base32 key for testing
# decode_otp_secret_and_generate("JBSWY3DPEHPK3PXP")
