import com.hp.hpl.jena.rdf.model.*;
import com.hp.hpl.jena.query.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

/**
 * Menjalankan banyak query SPARQL terhadap satu file OWL/RDF (tanpa reasoner;
 * gunakan file *_inferred.owl agar hasil Pellet ikut terbaca).
 *
 * Pakai:  java -cp <jar-jena>:tools/java Sparql <file.owl> <queries.txt>
 * Format queries.txt: blok dipisah baris "### <ID>". Keluaran: per blok
 *   ### <ID>
 *   kolom1\tkolom2...
 *   nilai1\tnilai2...
 */
public class Sparql {
  static String val(RDFNode n) {
    if (n == null) return "";
    if (n.isLiteral()) return n.asLiteral().getLexicalForm();
    if (n.isURIResource()) { String u = n.asResource().getURI(); int i = u.lastIndexOf('#'); return i >= 0 ? u.substring(i + 1) : u; }
    return n.toString();
  }
  public static void main(String[] a) throws Exception {
    Model m = ModelFactory.createDefaultModel();
    try (InputStream in = new FileInputStream(a[0])) { m.read(in, null, "RDF/XML"); }
    String all = new String(Files.readAllBytes(Paths.get(a[1])), "UTF-8");
    PrintStream out = new PrintStream(System.out, true, "UTF-8");
    for (String blk : all.split("(?m)^### ")) {
      if (blk.trim().isEmpty()) continue;
      int nl = blk.indexOf('\n'); String id = blk.substring(0, nl).trim(); String q = blk.substring(nl + 1);
      out.println("### " + id);
      try {
        QueryExecution qe = QueryExecutionFactory.create(QueryFactory.create(q, Syntax.syntaxARQ), m);
        ResultSet rs = qe.execSelect(); List<String> vars = rs.getResultVars();
        out.println(String.join("\t", vars));
        while (rs.hasNext()) { QuerySolution s = rs.next(); List<String> row = new ArrayList<>();
          for (String v : vars) row.add(val(s.get(v)).replace('\t', ' ').replace('\n', ' ')); out.println(String.join("\t", row)); }
        qe.close();
      } catch (Exception e) { out.println("!ERROR\t" + e.getMessage().replace('\n', ' ')); }
    }
  }
}
