# ACLs with final flag
PUBLIC_ACL_F = "1FBFBFFF"
PRIVATE_ACL_F = "1C8C8CCC"
READONLY_ACL_F = "1FBF8CFF"

# ACLs without final flag set
PUBLIC_ACL = "0FBFBFFF"
INACCESSIBLE_ACL = "40000000"
STICKY_BIT_PUB_ACL = "3FFFFFFF"

EACL_PUBLIC_READ_WRITE = "eacl-public-read-write"

# Regex patterns of status codes of Container service
CONTAINER_NOT_FOUND = "code = 3072.*message = container not found"


# Regex patterns of status codes of Object service
MALFORMED_REQUEST = "code = 1024.*message = malformed request"
OBJECT_ACCESS_DENIED = "code = 2048.*message = access to object operation denied"
OBJECT_NOT_FOUND = "code = 2049.*message = object not found"
OBJECT_ALREADY_REMOVED = "code = 2052.*message = object already removed"
SESSION_NOT_FOUND = "code = 4096.*message = session token not found"
OUT_OF_RANGE = "code = 2053.*message = out of range"
EXPIRED_SESSION_TOKEN = "code = 4097.*message = expired session token"
# TODO: Due to https://github.com/nspcc-dev/neofs-node/issues/2092 we have to check only codes until fixed
# OBJECT_IS_LOCKED = "code = 2050.*message = object is locked"
# LOCK_NON_REGULAR_OBJECT = "code = 2051.*message = ..." will be available once 2092 is fixed
OBJECT_IS_LOCKED = "code = 2050"
LOCK_NON_REGULAR_OBJECT = "code = 2051"

LIFETIME_REQUIRED = "either expiration epoch of a lifetime is required"
LOCK_OBJECT_REMOVAL = "lock object removal"
LOCK_OBJECT_EXPIRATION = "lock object expiration: {expiration_epoch}; current: {current_epoch}"
INVALID_RANGE_ZERO_LENGTH = "invalid '{range}' range: zero length"
INVALID_RANGE_OVERFLOW = "invalid '{range}' range: uint64 overflow"
INVALID_OFFSET_SPECIFIER = "invalid '{range}' range offset specifier"
INVALID_LENGTH_SPECIFIER = "invalid '{range}' range length specifier"
