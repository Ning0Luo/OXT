#!/usr/bin/env python
"""
PyDHE - Diffie-Hellman Key Exchange in Python
Copyright (C) 2015 by Mark Loiseau

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import hashlib
from .crypto_tools import prf_512
from binascii import hexlify # For debug output
from .crypto_tools import egcd
from cryptography.hazmat.primitives.asymmetric.dsa import generate_parameters
from cryptography.hazmat.primitives.asymmetric.dsa import DSAParametersWithNumbers
from cryptography.hazmat.backends import default_backend

# If a secure random number generator is unavailable, exit with an error.
try:
	import ssl
	random_function = ssl.RAND_bytes
	random_provider = "Python SSL"
except (AttributeError, ImportError):
	import OpenSSL
	random_function = OpenSSL.rand.bytes
	random_provider = "OpenSSL"

class DiffieHellman(object):
	"""
	A reference implementation of the Diffie-Hellman protocol.
	By default, this class uses the 6144-bit MODP Group (Group 17) from RFC 3526.
	This prime is sufficient to generate an AES 256 key when used with
	a 540+ bit exponent.
	"""

	def __init__(self,generator=2, group=17, keyLength=540):
		"""
		Generate the public and private keys.
		"""

		dsa_gen =generate_parameters(2048,backend=default_backend())

		dsa_g_n=dsa_gen.parameter_numbers()
		self.prime=dsa_g_n.q
		self.prime_p=dsa_g_n.p
		self.generator=dsa_g_n.g










	def genRandom(self,k,msg):
		"""
		Generate a random number with the msg
		"""

		_rand = int.from_bytes(prf_512(k,msg), byteorder="big")% self.prime
		return _rand


	def genPrivateKey(self,k, msg):
		return self.genRandom(k,msg)

	def genPublicKey(self, privateKey):

		return pow(self.generator, privateKey, self.prime_p)



	def genSecret(self, privateKey, otherKey):
		"""
		Check to make sure the public key is valid, then combine it with the
		private key to generate a shared secret.
		"""

		sharedSecret = pow(otherKey, privateKey, self.prime_p)
		return sharedSecret



	def genKey(self, privateKey,otherKey):
		"""
		Derive the shared secret, then hash it to obtain the shared key.
		"""
		self.sharedSecret = self.genSecret(privateKey, otherKey)

		# Convert the shared secret (int) to an array of bytes in network order
		# Otherwise hashlib can't hash it.
		try:
			_sharedSecretBytes = self.sharedSecret.to_bytes(
				self.sharedSecret.bit_length() // 8 + 1, byteorder="big")
		except AttributeError:
			_sharedSecretBytes = str(self.sharedSecret)

		s = hashlib.sha256()
		s.update(bytes(_sharedSecretBytes))
		self.key = s.digest()

	def getKey(self):
		"""
		Return the shared secret key
		"""
		return self.key



if __name__=="__main__":
	"""
	Run an example Diffie-Hellman exchange
	"""
	a = DiffieHellman()
	b = DiffieHellman()

	a.genKey(b.publicKey)
	b.genKey(a.publicKey)

	#a.showParams()
	#a.showResults()
	#b.showParams()
	#b.showResults()

	if(a.getKey() == b.getKey()):
		print("Shared keys match.")
		print("Key:", hexlify(a.key))
	else:
		print("Shared secrets didn't match!")
		print("Shared secret A: ", a.genSecret(b.publicKey))
		print("Shared secret B: ", b.genSecret(a.publicKey))
