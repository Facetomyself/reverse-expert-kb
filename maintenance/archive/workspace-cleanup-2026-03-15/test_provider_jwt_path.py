from email_providers.cloudflare import CloudflareEmailProvider

p = CloudflareEmailProvider()
p._address = 'tmailtavilybfiopzoz@zhangxuemin.work'
# Fill in JWT from runtime by scraping it from worker? impossible after the fact unless stored.
# So this script is meant to be edited with a real JWT before use.
print('SET_JWT_MANUALLY')
