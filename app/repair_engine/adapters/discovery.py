class DiscoveryAdapter:
    """
    Adapter layer between the Repair Engine and existing discovery/enrichment systems.

    Future repair modules should call this adapter instead of directly importing
    website discovery, email discovery, AI enrichment, or intelligence modules.
    """

    def recover_website(self, business):
        raise NotImplementedError("Website recovery adapter is not implemented yet.")

    def recover_email(self, business):
        raise NotImplementedError("Email recovery adapter is not implemented yet.")

    def recover_phone(self, business):
        raise NotImplementedError("Phone recovery adapter is not implemented yet.")

    def recover_social_profiles(self, business):
        raise NotImplementedError("Social profile recovery adapter is not implemented yet.")

    def recover_hours(self, business):
        raise NotImplementedError("Hours recovery adapter is not implemented yet.")

    def recover_images(self, business):
        raise NotImplementedError("Image recovery adapter is not implemented yet.")
