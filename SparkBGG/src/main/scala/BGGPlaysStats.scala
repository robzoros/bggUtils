import org.apache.spark.sql.{Dataset, SparkSession}
import org.apache.spark.sql.functions._

//import scala.language.postfixOps

/**
  * Created by utad on 6/17/17.
  * Algoritmo para inferencia de etiquetas de InceptionV3 desde Flickr
  */
object BGGPlaysStats {

  def main(args: Array[String]) {

    val fichero = args.toList match {
      case Nil => "hdfs://master.spark.tfm:9000/user/utad/fichero.csv"
      case arg :: Nil => arg
      case _ => Nil
    }

    if (fichero == Nil) {
      println("Uso: spark-submit \\\n  --class BGGPlaysStats \\\n  --master url-master \\\n  url-jar/sparkbgg_2.11-1.0.jar [fichero]")
      System.exit(1)
    }

    println("Fichero lectura: " + fichero)
    val spark = SparkSession
      .builder
      .appName("BGG Game Played Stats")
      .getOrCreate

    import spark.implicits._

    // Leemos fichero csv con las partidas
    val gamesPlayedDS = spark.read.json(fichero.toString).as[BGGPlay]

    // Totales
    val totals = gamesPlayedDS.agg(sum($"quantity") as "totalQ", sum($"length") as "totalL").collect()(0)
    val quantity:Long = totals.getAs("totalQ")
    val duration:Long = totals.getAs("totalL")
    println("quantity: " + quantity + ", duration: " + duration)

    // Totales por juego
    val totalsByGame = gamesPlayedDS.groupBy("game").agg(sum($"quantity") as "totalQ", sum($"length") as "totalL").sort($"totalL".desc).collect
    totalsByGame.foreach(r => println("Game: " + r.getAs("game") + ", quantity: " + r.getAs("totalQ") + ", duration: " + r.getAs("totalL")))

    //Totales por Amigo
    val friends = gamesPlayedDS.flatMap(r => r.players).filter(_ != "").distinct.collect
    def totalPorAmigo(ds: Dataset[BGGPlay], friend: String) : FriendStats = {
      val totalFriend = ds.filter(r => r.players.contains(friend))
                          .agg(sum($"quantity") as "totalQ", sum($"length") as "totalL")
                          .collect()(0)
      return FriendStats(friend, totalFriend.getAs("totalQ"), totalFriend.getAs("totalL"))
    }

    spark.sparkContext.parallelize(friends.map(f => totalPorAmigo(gamesPlayedDS, f)))
      .toDS()
      .sort($"length".desc)
      .collect
      .foreach(println(_))

  }

}
