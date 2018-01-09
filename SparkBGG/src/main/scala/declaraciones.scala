

/**
  * Created by utad on 6/18/17.
  */

// Definimos clases para los datasets
case class BGGPlay(date: String, quantity: BigInt, length: BigInt, location: String, game: String, gameId: String, players: Array[String])
case class FriendStats(name: String, quantity: Long, length: Long)
