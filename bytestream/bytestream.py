BIT_PER_BYTE = 8



def bin2bytes(bin: str) -> bytes:
  """
  Convert a bitstring into 'bytes'.

  Args:
    bin: A string containing only '0' and '1'

  Return:
    A bytes array

  Example:
    bin2bytes("01000001") == b"\x00A"
  """

  # Pad bytestream
  padding = len(bin) % BIT_PER_BYTE
  if padding != 0:
    padding = BIT_PER_BYTE - padding
  bin += "0" * padding

  # Store padding size
  bytestream = padding.to_bytes(1, "little")

  # Store bitstring
  for i in range(0, len(bin), BIT_PER_BYTE):
    bytestream += int(bin[i:i+BIT_PER_BYTE], 2).to_bytes(1, "little")

  return bytestream



def bytes2bin(bytestream: bytes) -> str:
  """
  Convert 'bytes' into a bitstring.

  Args:
    bytestream: A bytes array

  Return:
    A string containing only '0' and '1'

  Example:
    bytes2bin(b"\x00A") == "01000001"
  """

  # Restore padding size
  padding = int(bytestream[0])

  # Restore bitstring
  bin = ""
  for char in bytestream[1:]:
    bin += f"{char:0{BIT_PER_BYTE}b}"

  return bin[:-padding] if padding != 0 else bin
